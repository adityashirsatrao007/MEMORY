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

try:
    engine = create_engine(DATABASE_URL)
    # Test connection
    with engine.connect() as conn:
        pass
except Exception as e:
    logger.warning(f"Could not connect to PostgreSQL ({e}). Falling back to SQLite (test_licenses.db)")
    DATABASE_URL = "sqlite:///test_licenses.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

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
# ─── Email (Resend API) ───

RESEND_API = "https://api.resend.com/emails"

def send_email(to: str, subject: str, body: str) -> bool:
    if RESEND_API_KEY:
        try:
            payload = json.dumps({"from": EMAIL_FROM, "to": to, "subject": subject, "text": body}).encode()
            req = UrlRequest(RESEND_API, data=payload, method="POST")
            req.add_header("Authorization", f"Bearer {RESEND_API_KEY}")
            req.add_header("Content-Type", "application/json")
            req.add_header("User-Agent", "memory-license-server/1.0")
            with urlopen(req, timeout=15) as resp:
                resp_body = resp.read().decode()
                logger.info(f"Email sent via Resend to {to}: {subject} ({resp.status}) {resp_body}")
                return True
        except Exception as e:
            logger.error(f"Resend failed to send email to {to}: {e}. Trying SMTP fallback...")

    # Fallback to SMTP
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM", "noreply@memory.dev")

    if smtp_host and smtp_user and smtp_pass:
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(body, "plain", "utf-8")
            msg["Subject"] = subject
            msg["From"] = smtp_from
            msg["To"] = to
            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as s:
                s.starttls()
                s.login(smtp_user, smtp_pass)
                s.send_message(msg)
            logger.info(f"Email sent via SMTP to {to}: {subject}")
            return True
        except Exception as e:
            logger.error(f"SMTP fallback failed to {to}: {e}")
            return False

    logger.info(f"[EMAIL DISABLED] Would send to {to}: {subject} (Resend failed, SMTP config missing)")
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

# ─── Export Endpoint ───

@app.get("/export-signups-csv")
def export_signups_csv(token: str, db: Session = Depends(get_db)):
    if token != ADMIN_TOKEN:
        raise HTTPException(401, "Unauthorized")
        
    import io
    import csv
    from fastapi.responses import Response

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(["Email", "Name", "License Key", "Tier", "Max Machines", "Issued At", "Expires At", "Revoked", "Activations Count"])
    
    licenses = db.query(License).join(User).all()
    for lk in licenses:
        writer.writerow([
            lk.user.email if lk.user else "",
            lk.user.name if lk.user else "",
            lk.license_key,
            lk.tier,
            lk.max_machines,
            lk.issued_at.isoformat() if lk.issued_at else "",
            lk.expires_at.isoformat() if lk.expires_at else "never",
            lk.revoked,
            len(lk.activations)
        ])
        
    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=signups.csv"
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8443"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
