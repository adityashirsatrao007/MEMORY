import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add license-server directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../tools/license-server")))

# Setup test environment variables
os.environ["DATABASE_URL"] = "sqlite:///test_licenses.db"
os.environ["LICENSE_ADMIN_TOKEN"] = "test-admin-token"
os.environ["OWNER_EMAIL"] = "admin@example.com"
os.environ["MEMORY_NON_COMMERCIAL"] = "1"

from main import app, get_db
from models import Base, User, License, Machine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set up test SQLite database
engine = create_engine("sqlite:///test_licenses.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    client.cookies.clear()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_health():
    response = client.get("/", follow_redirects=False)
    # Redirects to /admin
    assert response.status_code == 307 or response.status_code == 302
    assert "/admin" in response.headers.get("location", "")

def test_request_trial_success():
    payload = {"email": "test@example.com", "name": "Test User"}
    response = client.post("/request-trial", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "license_key" not in data  # Loophole check: key MUST not be leaked
    assert data["tier"] == "trial"
    assert data["email"] == "test@example.com"
    
    # Check that the license exists in the DB
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    license = db.query(License).filter(License.user_id == user.id).first()
    assert license is not None
    assert license.tier == "trial"
    db.close()

def test_request_trial_duplicate():
    payload = {"email": "test@example.com", "name": "Test User"}
    response = client.post("/request-trial", json=payload)
    assert response.status_code == 200
    
    # Second request should fail with 400
    response = client.post("/request-trial", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_admin_login():
    # Invalid token
    response = client.post("/admin/login", json={"email": "admin@example.com", "token": "wrong-token"})
    assert response.status_code == 401
    
    # Valid token
    response = client.post("/admin/login", json={"email": "admin@example.com", "token": "test-admin-token"}, follow_redirects=False)
    assert response.status_code == 302
    assert "admin_session" in response.headers.get("set-cookie", "")

def test_activate_invalid_key():
    response = client.post("/activate", json={
        "license_key": "INVALID-KEY-1234",
        "machine_fingerprint": "test-fingerprint",
        "hostname": "test-host",
        "platform": "Linux"
    })
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_activate_verify_refresh_revoke_flow():
    # 1. Request trial key (need to extract it from DB since it's not in the response)
    trial_payload = {"email": "user@example.com", "name": "User"}
    response = client.post("/request-trial", json=trial_payload)
    assert response.status_code == 200
    
    db = TestingSessionLocal()
    user = db.query(User).filter(User.email == "user@example.com").first()
    license = db.query(License).filter(License.user_id == user.id).first()
    license_key = license.license_key
    db.close()
    
    # 2. Activate
    activate_payload = {
        "license_key": license_key,
        "machine_fingerprint": "machine-123",
        "hostname": "my-host",
        "platform": "Darwin"
    }
    response = client.post("/activate", json=activate_payload)
    assert response.status_code == 200
    activate_data = response.json()
    token = activate_data["token"]
    assert activate_data["tier"] == "trial"
    
    # 3. Verify
    verify_payload = {
        "token": token,
        "machine_fingerprint": "machine-123"
    }
    response = client.post("/verify", json=verify_payload)
    assert response.status_code == 200
    assert response.json()["valid"] is True
    
    # Verify with mismatched fingerprint
    response = client.post("/verify", json={"token": token, "machine_fingerprint": "wrong-machine"})
    assert response.status_code == 200
    assert response.json()["valid"] is False
    assert "fingerprint mismatch" in response.json()["message"].lower()

    # 4. Refresh token
    refresh_payload = {
        "token": token,
        "machine_fingerprint": "machine-123"
    }
    response = client.post("/refresh", json=refresh_payload)
    assert response.status_code == 200
    new_token = response.json()["token"]
    assert new_token != token
    
    # Verify new token passes
    response = client.post("/verify", json={"token": new_token, "machine_fingerprint": "machine-123"})
    assert response.status_code == 200
    assert response.json()["valid"] is True
    
    # Verify old token is now invalid/inactive
    response = client.post("/verify", json={"token": token, "machine_fingerprint": "machine-123"})
    assert response.status_code == 200
    assert response.json()["valid"] is False

    # 5. Revoke license
    response = client.post("/revoke", json={"license_key": license_key})
    assert response.status_code == 200
    
    # Verify license is revoked
    response = client.post("/verify", json={"token": new_token, "machine_fingerprint": "machine-123"})
    assert response.status_code == 200
    assert response.json()["valid"] is False
    assert "revoked" in response.json()["message"].lower()

def test_admin_actions():
    gen_payload = {
        "email": "customer@example.com",
        "tier": "pro",
        "duration_days": 30,
        "max_machines": 2
    }
    # Unauthorized generate
    response = client.post("/admin/generate", json=gen_payload)
    assert response.status_code == 401

    # Login to get cookie
    login_response = client.post("/admin/login", json={"email": "admin@example.com", "token": "test-admin-token"}, follow_redirects=False)
    assert login_response.status_code == 302

    # Authorized generate (client automatically uses session cookie)
    response = client.post("/admin/generate", json=gen_payload)
    assert response.status_code == 200
    gen_data = response.json()
    license_key = gen_data["license_key"]
    assert gen_data["tier"] == "pro"
    assert gen_data["max_machines"] == 2
    
    # List licenses
    response = client.get("/admin/licenses")
    assert response.status_code == 200
    licenses = response.json()
    assert any(l["license_key"] == license_key for l in licenses)
    
    # Stats
    response = client.get("/admin/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["licenses"]["total"] >= 1

    # Activate machine 1
    client.post("/activate", json={
        "license_key": license_key,
        "machine_fingerprint": "mac-1",
        "hostname": "h1"
    })
    
    # Activate machine 2
    client.post("/activate", json={
        "license_key": license_key,
        "machine_fingerprint": "mac-2",
        "hostname": "h2"
    })
    
    # Activate machine 3 (exceed max_machines = 2)
    response = client.post("/activate", json={
        "license_key": license_key,
        "machine_fingerprint": "mac-3",
        "hostname": "h3"
    })
    assert response.status_code == 403
    assert "maximum activations" in response.json()["detail"].lower()

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
