"""
MEMORY License Activation Server
FastAPI + PostgreSQL + JWT (RS256) + Email delivery
"""
import os
import re
import uuid
import json
import secrets
import hashlib
import logging
from urllib.request import Request as UrlRequest, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager

import jwt
from fastapi import FastAPI, HTTPException, Depends, Request, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, sessionmaker

from models import Base, User, License, Machine, Activation

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("memory-license")

# ─── Config ───
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://memory:memory@localhost:5432/memory_licenses")
PRIVATE_KEY = os.getenv("LICENSE_PRIVATE_KEY", "").replace("\\n", "\n")
PUBLIC_KEY = os.getenv("LICENSE_PUBLIC_KEY", "").replace("\\n", "\n")
ADMIN_TOKEN = os.getenv("LICENSE_ADMIN_TOKEN", "change-me-in-production")
if ADMIN_TOKEN == "change-me-in-production":
    logger.warning("SECURITY WARNING: Using default ADMIN_TOKEN. Please set LICENSE_ADMIN_TOKEN environment variable in production!")
OWNER_EMAIL = os.getenv("OWNER_EMAIL", "adityashirsatrao007@gmail.com")
SESSION_SECRET = os.getenv("SESSION_SECRET", secrets.token_hex(32))
ISSUER = "memory-license-server"

# Resend email config (optional — if unset, keys print to console/log)
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "MEMORY <onboarding@resend.dev>")

# Generate keys on first run if not provided
if not PRIVATE_KEY:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    PRIVATE_KEY = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    PUBLIC_KEY = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    print("=== GENERATED NEW KEY PAIR ===")
    print("PRIVATE_KEY=" + PRIVATE_KEY.replace("\n", "\\n"))
    print("PUBLIC_KEY=" + PUBLIC_KEY.replace("\n", "\\n"))

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

# ─── Helpers ───

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def make_license_key(tier: str = "TRIAL") -> str:
    parts = [secrets.token_hex(2).upper() for _ in range(3)]
    return f"MEM-{tier}-{parts[0]}-{parts[1]}-{parts[2]}"

def make_machine_fingerprint(data: dict) -> str:
    raw = json.dumps(data, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

def sign_jwt(license_key: str, tier: str, email: str, machine_fp: str,
             expires_at: datetime | None) -> str:
    payload = {
        "license_key": license_key,
        "tier": tier,
        "email": email,
        "machine_fp": machine_fp,
        "iss": ISSUER,
        "iat": datetime.now(timezone.utc),
        "jti": str(uuid.uuid4()),
    }
    if expires_at:
        payload["exp"] = expires_at
    else:
        payload["exp"] = datetime.now(timezone.utc) + timedelta(days=3650)
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def verify_jwt(token: str) -> dict:
    return jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], issuer=ISSUER)

def is_future(dt: datetime | None) -> bool:
    if not dt:
        return False
    if dt.tzinfo is not None:
        return dt > datetime.now(timezone.utc)
    return dt > datetime.now(timezone.utc).replace(tzinfo=None)

def is_past(dt: datetime | None) -> bool:
    if not dt:
        return False
    if dt.tzinfo is not None:
        return dt < datetime.now(timezone.utc)
    return dt < datetime.now(timezone.utc).replace(tzinfo=None)


# ─── Session (admin cookie auth) ───

def make_session_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(days=30),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SESSION_SECRET, algorithm="HS256")

def verify_session(token: str) -> dict | None:
    try:
        return jwt.decode(token, SESSION_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None

# ─── Email (Resend API) ───

RESEND_API = "https://api.resend.com/emails"

def send_email(to: str, subject: str, body: str) -> bool:
    if not RESEND_API_KEY:
        logger.info(f"[EMAIL DISABLED] Would send to {to}: {subject}")
        return False
    try:
        payload = json.dumps({"from": EMAIL_FROM, "to": to, "subject": subject, "text": body}).encode()
        req = UrlRequest(RESEND_API, data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {RESEND_API_KEY}")
        req.add_header("Content-Type", "application/json")
        req.add_header("User-Agent", "memory-license-server/1.0")
        with urlopen(req, timeout=15) as resp:
            resp_body = resp.read().decode()
            logger.info(f"Email sent to {to}: {subject} ({resp.status}) {resp_body}")
            return True
    except HTTPError as e:
        body = e.read().decode()
        logger.error(f"Email failed to {to}: {e.code} {body}")
        return False
    except URLError as e:
        logger.error(f"Email failed to {to}: {e}")
        return False
    except Exception as e:
        logger.error(f"Email failed to {to}: {e}")
        return False

# ─── Schemas ───

class ActivateRequest(BaseModel):
    license_key: str
    machine_fingerprint: str
    hostname: str = ""
    platform: str = ""

class ActivateResponse(BaseModel):
    token: str
    tier: str
    expires_at: str | None

class VerifyRequest(BaseModel):
    token: str
    machine_fingerprint: str

class VerifyResponse(BaseModel):
    valid: bool
    tier: str | None = None
    message: str = ""

class RevokeRequest(BaseModel):
    license_key: str

class AdminGenerateRequest(BaseModel):
    email: str
    tier: str = "trial"
    duration_days: int = 3
    max_machines: int = 1

# ─── App ───

app = FastAPI(title="MEMORY License Server", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return RedirectResponse(url="/admin")

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

class RequestTrialRequest(BaseModel):
    email: str
    name: str = ""

@app.post("/request-trial")
def request_trial(req: RequestTrialRequest, db: Session = Depends(get_db)):
    lk = make_license_key("TRIAL")
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        user = User(email=req.email, name=req.name or req.email.split("@")[0])
        db.add(user)
        db.flush()
    existing = db.query(License).filter(
        License.user_id == user.id, License.tier == "trial", License.revoked == False
    ).first()
    if existing and existing.expires_at and is_future(existing.expires_at):
        raise HTTPException(400, "Active trial already exists for this email")
    expires_at = datetime.now(timezone.utc) + timedelta(days=3)
    license = License(
        license_key=lk, user_id=user.id, tier="trial",
        max_machines=1, expires_at=expires_at
    )
    db.add(license)
    db.commit()

    body = (
        f"Your MEMORY trial license:\n\n"
        f"  Key: {lk}\n"
        f"  Tier: Trial (3 days)\n"
        f"  Expires: {expires_at.strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        f"Activate: memory license activate --key {lk}\n"
    )
    sent = send_email(req.email, "Your MEMORY Trial License", body)
    if not sent:
        logger.info(f"Trial key for {req.email}: {lk}")

    return {
        "tier": "trial",
        "expires_at": expires_at.isoformat(),
        "email": req.email,
        "email_delivered": sent
    }

@app.post("/activate", response_model=ActivateResponse)
def activate(req: ActivateRequest, db: Session = Depends(get_db)):
    license = db.query(License).filter(License.license_key == req.license_key).first()
    if not license:
        raise HTTPException(404, "License key not found")
    if license.revoked:
        raise HTTPException(403, "License has been revoked")
    if license.expires_at and is_past(license.expires_at):
        raise HTTPException(410, "License has expired")

    machine = db.query(Machine).filter(Machine.fingerprint == req.machine_fingerprint).first()
    if not machine:
        machine = Machine(
            fingerprint=req.machine_fingerprint,
            hostname=req.hostname or "",
            platform=req.platform or ""
        )
        db.add(machine)
        db.flush()

    activation_count = db.query(func.count(Activation.id)).filter(
        Activation.license_id == license.id,
        Activation.active == True
    ).scalar()

    if activation_count >= license.max_machines:
        existing = db.query(Activation).filter(
            Activation.license_id == license.id,
            Activation.machine_id == machine.id,
            Activation.active == True
        ).first()
        if not existing:
            raise HTTPException(403, f"Maximum activations ({license.max_machines}) reached")

    token = sign_jwt(
        license_key=license.license_key,
        tier=license.tier,
        email=license.user.email if license.user else "",
        machine_fp=req.machine_fingerprint,
        expires_at=license.expires_at
    )

    activation = db.query(Activation).filter(
        Activation.license_id == license.id,
        Activation.machine_id == machine.id
    ).first()

    if activation:
        activation.token = token
        activation.last_verified = datetime.now(timezone.utc)
        activation.active = True
    else:
        activation = Activation(
            license_id=license.id,
            machine_id=machine.id,
            token=token
        )
        db.add(activation)

    machine.last_seen = datetime.now(timezone.utc)
    db.commit()

    return ActivateResponse(
        token=token,
        tier=license.tier,
        expires_at=license.expires_at.isoformat() if license.expires_at else None
    )

@app.post("/verify", response_model=VerifyResponse)
def verify(req: VerifyRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_jwt(req.token)
    except jwt.ExpiredSignatureError:
        return VerifyResponse(valid=False, message="Token expired")
    except jwt.InvalidTokenError as e:
        return VerifyResponse(valid=False, message=f"Invalid token: {e}")

    if payload.get("machine_fp") != req.machine_fingerprint:
        return VerifyResponse(valid=False, message="Machine fingerprint mismatch")

    license = db.query(License).filter(License.license_key == payload["license_key"]).first()
    if not license:
        return VerifyResponse(valid=False, message="License not found")
    if license.revoked:
        return VerifyResponse(valid=False, message="License revoked")
    if license.expires_at and is_past(license.expires_at):
        return VerifyResponse(valid=False, message="License expired")

    activation = db.query(Activation).filter(
        Activation.license_id == license.id,
        Activation.token == req.token,
        Activation.active == True
    ).first()
    if not activation:
        return VerifyResponse(valid=False, message="Activation not found or inactive")

    activation.last_verified = datetime.now(timezone.utc)
    db.commit()

    return VerifyResponse(valid=True, tier=license.tier, message="OK")

@app.post("/refresh")
def refresh(req: VerifyRequest, db: Session = Depends(get_db)):
    try:
        payload = verify_jwt(req.token)
    except jwt.ExpiredSignatureError:
        payload = jwt.decode(req.token, PUBLIC_KEY, algorithms=["RS256"],
                             options={"verify_exp": False})
    except jwt.InvalidTokenError as e:
        raise HTTPException(400, f"Invalid token: {e}")

    if payload.get("machine_fp") != req.machine_fingerprint:
        raise HTTPException(403, "Machine fingerprint mismatch")

    license = db.query(License).filter(License.license_key == payload["license_key"]).first()
    if not license or license.revoked:
        raise HTTPException(403, "License invalid or revoked")

    activation = db.query(Activation).filter(
        Activation.license_id == license.id,
        Activation.token == req.token,
        Activation.active == True
    ).first()
    if not activation:
        raise HTTPException(403, "Activation not found or inactive")

    new_token = sign_jwt(
        license_key=license.license_key,
        tier=license.tier,
        email=payload.get("email", ""),
        machine_fp=req.machine_fingerprint,
        expires_at=license.expires_at
    )

    activation.token = new_token
    activation.last_verified = datetime.now(timezone.utc)
    db.commit()

    return {"token": new_token, "tier": license.tier}

@app.post("/revoke")
def revoke(req: RevokeRequest, db: Session = Depends(get_db)):
    license = db.query(License).filter(License.license_key == req.license_key).first()
    if not license:
        raise HTTPException(404, "License not found")
    license.revoked = True
    db.query(Activation).filter(Activation.license_id == license.id).update({"active": False})
    db.commit()
    return {"status": "revoked", "license_key": req.license_key}

# ─── Admin Endpoints ───

def verify_admin(admin_session: str = ""):
    session = verify_session(admin_session)
    if session and session.get("email") == OWNER_EMAIL:
        return session["email"]
    raise HTTPException(401, "Unauthorized")

@app.post("/admin/generate")
def admin_generate(req: AdminGenerateRequest, admin_session: str = Cookie(default=""), db: Session = Depends(get_db)):
    verify_admin(admin_session)
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        user = User(email=req.email, name=req.email.split("@")[0])
        db.add(user)
        db.flush()
    tier = req.tier.upper()
    if tier not in ("TRIAL", "PRO", "ENTERPRISE"):
        raise HTTPException(400, "Invalid tier. Use: trial, pro, enterprise")
    expires_at = None
    if req.duration_days > 0:
        expires_at = datetime.now(timezone.utc) + timedelta(days=req.duration_days)
    lk = License(
        license_key=make_license_key(tier),
        user_id=user.id,
        tier=tier.lower(),
        max_machines=req.max_machines,
        expires_at=expires_at
    )
    db.add(lk)
    db.commit()
    return {
        "license_key": lk.license_key,
        "tier": lk.tier,
        "expires_at": lk.expires_at.isoformat() if lk.expires_at else "never",
        "max_machines": lk.max_machines,
        "user": req.email
    }

@app.post("/admin/send-license")
def admin_send_license(req: AdminGenerateRequest, admin_session: str = Cookie(default=""), db: Session = Depends(get_db)):
    verify_admin(admin_session)
    license = db.query(License).join(User).filter(User.email == req.email).order_by(License.issued_at.desc()).first()
    if not license:
        raise HTTPException(404, "No license found for this email")
    tier_display = license.tier.upper()
    body = (
        f"Your MEMORY {tier_display} license:\n\n"
        f"  Key: {license.license_key}\n"
        f"  Tier: {tier_display}\n"
        f"  Expires: {license.expires_at.strftime('%Y-%m-%d %H:%M UTC') if license.expires_at else 'Never'}\n\n"
        f"Activate: memory license activate --key {license.license_key}\n"
    )
    sent = send_email(req.email, f"Your MEMORY {tier_display} License", body)
    if not sent:
        logger.info(f"License {license.license_key} for {req.email} (email disabled)")
    return {"status": "sent" if sent else "printed", "license_key": license.license_key, "email": req.email, "delivered": sent}

@app.get("/admin/licenses")
def admin_list(admin_session: str = Cookie(default=""), db: Session = Depends(get_db)):
    verify_admin(admin_session)
    licenses = db.query(License).all()
    result = []
    for lk in licenses:
        result.append({
            "license_key": lk.license_key,
            "tier": lk.tier,
            "email": lk.user.email if lk.user else "",
            "issued_at": lk.issued_at.isoformat(),
            "expires_at": lk.expires_at.isoformat() if lk.expires_at else "never",
            "revoked": lk.revoked,
            "activations": len(lk.activations)
        })
    return result

@app.get("/admin/activations")
def admin_activations(admin_session: str = Cookie(default=""), db: Session = Depends(get_db)):
    verify_admin(admin_session)
    activations = db.query(Activation).all()
    result = []
    for a in activations:
        result.append({
            "id": str(a.id),
            "license_key": a.license.license_key if a.license else "",
            "email": a.license.user.email if a.license and a.license.user else "",
            "tier": a.license.tier if a.license else "",
            "machine_fingerprint": a.machine.fingerprint[:16] + "..." if a.machine else "",
            "hostname": a.machine.hostname if a.machine else "",
            "platform": a.machine.platform if a.machine else "",
            "activated_at": a.activated_at.isoformat(),
            "last_verified": a.last_verified.isoformat() if a.last_verified else "",
            "active": a.active
        })
    return result

@app.get("/admin/stats")
def admin_stats(admin_session: str = Cookie(default=""), db: Session = Depends(get_db)):
    verify_admin(admin_session)
    total_licenses = db.query(func.count(License.id)).scalar()
    active_licenses = db.query(func.count(License.id)).filter(
        License.revoked == False,
        (License.expires_at > datetime.now(timezone.utc)) | (License.expires_at == None)
    ).scalar()
    expired = db.query(func.count(License.id)).filter(
        License.expires_at < datetime.now(timezone.utc)
    ).scalar()
    revoked = db.query(func.count(License.id)).filter(License.revoked == True).scalar()
    total_activations = db.query(func.count(Activation.id)).scalar()
    live_activations = db.query(func.count(Activation.id)).filter(Activation.active == True).scalar()
    total_users = db.query(func.count(User.id)).scalar()
    total_machines = db.query(func.count(Machine.id)).scalar()
    by_tier = db.query(License.tier, func.count(License.id)).group_by(License.tier).all()
    return {
        "licenses": {"total": total_licenses, "active": active_licenses, "expired": expired, "revoked": revoked},
        "activations": {"total": total_activations, "live": live_activations},
        "users": total_users,
        "machines": total_machines,
        "by_tier": {tier: count for tier, count in by_tier}
    }

@app.post("/admin/reset-db-dangerous")
def admin_reset_db_dangerous(token: str, db: Session = Depends(get_db)):
    if token != ADMIN_TOKEN:
        raise HTTPException(401, "Unauthorized")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "Database reset successfully"}


@app.get("/admin/login", response_class=HTMLResponse)
def admin_login_page():
    return HTMLResponse(ADMIN_LOGIN_HTML)

class LoginRequest(BaseModel):
    email: str
    token: str

@app.post("/admin/login")
def admin_login(req: LoginRequest):
    if req.email == OWNER_EMAIL and req.token == ADMIN_TOKEN:
        session_token = make_session_token(req.email)
        redirect = RedirectResponse(url="/admin", status_code=302)
        redirect.set_cookie(key="admin_session", value=session_token,
                           max_age=30*24*3600, httponly=True, samesite="lax")
        return redirect
    raise HTTPException(401, "Invalid credentials")

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(admin_session: str = Cookie(default="")):
    session = verify_session(admin_session)
    if not session:
        return HTMLResponse(ADMIN_LOGIN_HTML)
    return HTMLResponse(ADMIN_HTML)

@app.get("/admin/logout")
def admin_logout():
    redirect = RedirectResponse(url="/admin", status_code=302)
    redirect.delete_cookie(key="admin_session")
    return redirect

ADMIN_LOGIN_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MEMORY License Admin — Login</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #FAF9F5; color: #3D3D3A; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
  .card { background: #fff; border: 1px solid #D1CFC5; border-radius: 12px; padding: 32px; width: 380px; }
  h1 { font-family: ui-serif, Georgia, serif; font-weight: 500; font-size: 24px; margin-bottom: 4px; }
  p { color: #87867F; font-size: 14px; margin-bottom: 20px; }
  label { display: block; font-size: 13px; font-weight: 600; margin: 12px 0 4px; }
  input { width: 100%; padding: 10px 12px; border: 1px solid #D1CFC5; border-radius: 8px; font-size: 14px; }
  button { background: #141413; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 16px; width: 100%; }
  button:hover { background: #D97757; }
  .error { background: #F8E0DE; color: #B85450; padding: 8px 12px; border-radius: 6px; font-size: 13px; margin-top: 8px; display: none; }
</style>
</head>
<body>
<div class="card">
  <h1>MEMORY License Admin</h1>
  <p>Enter your admin credentials to continue.</p>
  <form id="login-form" method="post" action="/admin/login">
    <label>Email</label>
    <input type="email" name="email" value="adityashirsatrao007@gmail.com" required>
    <label>Admin Token</label>
    <input type="password" name="token" required placeholder="Enter admin token">
    <button type="submit">Sign In</button>
    <div class="error" id="error-msg">Invalid credentials. Try again.</div>
  </form>
</div>
<script>
document.getElementById('login-form').addEventListener('submit', async function(e) {
  e.preventDefault();
  var form = e.target;
  var errEl = document.getElementById('error-msg');
  try {
    var resp = await fetch('/admin/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: form.email.value, token: form.token.value})
    });
    if (resp.redirected) { window.location.href = resp.url; return; }
    if (!resp.ok) { errEl.style.display = 'block'; return; }
    var data = await resp.json();
    if (data.status === 'ok') { window.location.href = '/admin'; }
  } catch(e) { errEl.style.display = 'block'; }
});
</script>
</body>
</html>
"""

ADMIN_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MEMORY License Admin</title>
<script src="https://unpkg.com/htmx.org@2.0.0"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, sans-serif; background: #FAF9F5; color: #3D3D3A; padding: 32px; }
  .wrap { max-width: 1100px; margin: 0 auto; }
  h1 { font-family: ui-serif, Georgia, serif; font-weight: 500; font-size: 32px; }
  .top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
  .logout-btn { font-size: 12px; color: #B85450; text-decoration: none; padding: 6px 12px; border: 1px solid #B85450; border-radius: 6px; }
  .logout-btn:hover { background: #F8E0DE; }
  .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 24px; }
  .stat { background: #fff; border: 1px solid #D1CFC5; border-radius: 8px; padding: 16px; text-align: center; }
  .stat-num { font-size: 28px; font-weight: 700; color: #141413; }
  .stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: .5px; color: #87867F; margin-top: 4px; }
  .card { background: #fff; border: 1px solid #D1CFC5; border-radius: 12px; padding: 24px; margin-bottom: 24px; }
  .card h2 { font-size: 18px; margin-bottom: 16px; }
  label { display: block; font-size: 13px; font-weight: 600; margin: 8px 0 4px; }
  input, select { width: 100%; padding: 8px 12px; border: 1px solid #D1CFC5; border-radius: 6px; font-size: 14px; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  button { background: #141413; color: #fff; border: none; padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 12px; }
  button:hover { background: #D97757; }
  table { width: 100%; border-collapse: collapse; font-size: 11px; }
  th, td { padding: 5px 6px; text-align: left; border-bottom: 1px solid #E6E3DA; }
  th { font-family: monospace; font-size: 8px; text-transform: uppercase; color: #87867F; white-space: nowrap; }
  td { vertical-align: top; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 10px; font-weight: 600; white-space: nowrap; }
  .badge-ok { background: #E3F0D9; color: #5E7A47; }
  .badge-no { background: #F8E0DE; color: #B85450; }
  .badge-warn { background: #FDF3D0; color: #9A7D2A; }
  .badge-soft { background: #E6E3DA; color: #87867F; }
  .msg { margin-top: 8px; font-size: 13px; padding: 8px 12px; border-radius: 6px; }
  .msg-ok { background: #E3F0D9; color: #5E7A47; }
  .msg-er { background: #F8E0DE; color: #B85450; }
  .key { font-family: monospace; font-size: 14px; font-weight: 600; color: #141413; background: #F0EEE6; padding: 8px 12px; border-radius: 6px; display: inline-block; margin-top: 8px; }
  .tab-bar { display: flex; gap: 4px; margin-bottom: 16px; }
  .tab { padding: 8px 16px; border: 1px solid #D1CFC5; border-radius: 8px 8px 0 0; font-size: 12px; font-weight: 600; cursor: pointer; background: #F0EEE6; color: #87867F; }
  .tab.active { background: #fff; color: #141413; border-bottom-color: #fff; }
  .tab:hover { background: #E6E3DA; }
  .tab-content { display: none; }
  .tab-content.active { display: block; }
  .scroll { overflow-x: auto; }
  .mono { font-family: monospace; font-size: 10px; }
</style>
</head>
<body>
<div class="wrap">
  <div class="top-bar">
    <h1>MEMORY License Admin</h1>
    <a href="/admin/logout" class="logout-btn">Sign Out</a>
  </div>

  <div id="stats-bar" class="stats"></div>

  <div class="card">
    <h2>Generate License Key</h2>
    <form hx-post="/admin/generate" hx-target="#gen-result">
      <div class="row">
        <div><label>Email</label><input type="email" name="email" required placeholder="user@example.com"></div>
        <div><label>Tier</label><select name="tier"><option value="trial">Trial (3 days)</option><option value="pro">Pro (never expires)</option><option value="enterprise">Enterprise</option></select></div>
      </div>
      <div class="row">
        <div><label>Duration (days, 0 = never expires)</label><input type="number" name="duration_days" value="3"></div>
        <div><label>Max Machines</label><input type="number" name="max_machines" value="1"></div>
      </div>
      <button type="submit">Generate</button>
    </form>
    <div id="gen-result"></div>
  </div>

  <div class="card">
    <h2>Send License Key via Email</h2>
    <form hx-post="/admin/send-license" hx-target="#email-result">
      <div class="row">
        <div><label>Email</label><input type="email" name="email" required placeholder="user@example.com"></div>
      </div>
      <button type="submit">Send License Key</button>
    </form>
    <div id="email-result"></div>
  </div>

  <div class="card">
    <div class="tab-bar">
      <div class="tab active" onclick="switchTab('licenses-tab', this)">Licenses</div>
      <div class="tab" onclick="switchTab('activations-tab', this)">Activated Machines</div>
    </div>

    <div id="licenses-tab" class="tab-content active scroll">
      <button hx-get="/admin/licenses" hx-target="#licenses" style="background:transparent;color:#141413;border:1px solid #D1CFC5;padding:6px 14px;font-size:12px;margin-bottom:12px;">Refresh</button>
      <div id="licenses"><p style="color:#87867F;">Click refresh to load.</p></div>
    </div>

    <div id="activations-tab" class="tab-content scroll">
      <button hx-get="/admin/activations" hx-target="#activations" style="background:transparent;color:#141413;border:1px solid #D1CFC5;padding:6px 14px;font-size:12px;margin-bottom:12px;">Refresh</button>
      <div id="activations"><p style="color:#87867F;">Click refresh to load.</p></div>
    </div>
  </div>
</div>

<script>
function switchTab(id, btn) {
  document.querySelectorAll('.tab-content').forEach(function(t) { t.classList.remove('active'); });
  document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}

function loadStats() {
  fetch('/admin/stats').then(function(r) { return r.json(); }).then(function(d) {
    var html =
      '<div class="stat"><div class="stat-num">' + d.licenses.total + '</div><div class="stat-label">Total Licenses</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.licenses.active + '</div><div class="stat-label">Active</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.licenses.expired + '</div><div class="stat-label">Expired</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.licenses.revoked + '</div><div class="stat-label">Revoked</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.activations.live + '</div><div class="stat-label">Live Machines</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.machines + '</div><div class="stat-label">Total Machines</div></div>' +
      '<div class="stat"><div class="stat-num">' + d.users + '</div><div class="stat-label">Users</div></div>';
    document.getElementById('stats-bar').innerHTML = html;
  });
}
loadStats();

document.addEventListener('htmx:afterRequest', function(e) {
  var el = e.detail.elt;
  if (e.detail.xhr.status === 200 && el.id === 'gen-result') {
    var d = JSON.parse(e.detail.xhr.responseText);
    el.innerHTML = '<div class="msg msg-ok">Key generated</div><div class="key">' + d.license_key + '</div>';
    loadStats();
  }
  if (e.detail.xhr.status === 200 && el.id === 'email-result') {
    var d = JSON.parse(e.detail.xhr.responseText);
    el.innerHTML = '<div class="msg msg-ok">License sent to ' + d.email + (d.delivered ? ' (email)' : ' (printed to server log)') + '</div>';
  }
  if (e.detail.xhr.status === 200 && el.id === 'licenses') {
    var list = JSON.parse(e.detail.xhr.responseText);
    if (!list.length) { el.innerHTML = '<p style="color:#87867F;">No licenses yet.</p>'; return; }
    var h = '<table><tr><th>Key</th><th>Tier</th><th>Email</th><th>Issued</th><th>Expires</th><th>Status</th><th>Machines</th></tr>';
    list.forEach(function(l) {
      var status = l.revoked ? '<span class="badge badge-no">Revoked</span>' :
                   l.expires_at === 'never' ? '<span class="badge badge-ok">Active</span>' :
                   new Date(l.expires_at) < new Date() ? '<span class="badge badge-no">Expired</span>' :
                   '<span class="badge badge-ok">Active</span>';
      var machineBadge = parseInt(l.activations) > 0 ? '<span class="badge badge-ok">' + l.activations + '</span>' : '<span class="badge badge-soft">' + l.activations + '</span>';
      h += '<tr><td class="mono">' + l.license_key + '</td>' +
           '<td>' + l.tier + '</td><td>' + l.email + '</td>' +
           '<td style="font-size:10px;">' + new Date(l.issued_at).toLocaleDateString() + '</td>' +
           '<td style="font-size:10px;">' + (l.expires_at === 'never' ? 'Never' : new Date(l.expires_at).toLocaleDateString()) + '</td>' +
           '<td>' + status + '</td><td>' + machineBadge + '</td></tr>';
    });
    h += '</table>';
    el.innerHTML = h;
  }
  if (e.detail.xhr.status === 200 && el.id === 'activations') {
    var list = JSON.parse(e.detail.xhr.responseText);
    if (!list.length) { el.innerHTML = '<p style="color:#87867F;">No activations yet.</p>'; return; }
    var h = '<table><tr><th>License Key</th><th>Email</th><th>Tier</th><th>Hostname</th><th>Platform</th><th>Activated</th><th>Last Verified</th><th>Status</th></tr>';
    list.forEach(function(a) {
      var status = a.active ? '<span class="badge badge-ok">Live</span>' : '<span class="badge badge-no">Inactive</span>';
      h += '<tr><td class="mono">' + a.license_key + '</td>' +
           '<td>' + a.email + '</td><td>' + a.tier + '</td>' +
           '<td class="mono">' + (a.hostname || '-') + '</td>' +
           '<td style="font-size:10px;">' + (a.platform || '-') + '</td>' +
           '<td style="font-size:10px;">' + new Date(a.activated_at).toLocaleString() + '</td>' +
           '<td style="font-size:10px;">' + (a.last_verified ? new Date(a.last_verified).toLocaleString() : '-') + '</td>' +
           '<td>' + status + '</td></tr>';
    });
    h += '</table>';
    el.innerHTML = h;
  }
  if (e.detail.xhr.status !== 200 && e.detail.xhr.status !== 0) {
    el.innerHTML = '<div class="msg msg-er">' + (e.detail.xhr.responseJSON?.detail || 'Error') + '</div>';
  }
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8443"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
