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

# Admin login was removed

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

def test_export_signups_csv():
    # Unauthorized export
    response = client.get("/export-signups-csv?token=test-admin-token") # wait, wrong token first
    response = client.get("/export-signups-csv?token=wrong-token")
    assert response.status_code == 401
    
    # Generate some users and licenses by requesting a trial
    trial_payload = {"email": "customer@example.com", "name": "Customer"}
    client.post("/request-trial", json=trial_payload)
    
    # Authorized export
    response = client.get("/export-signups-csv?token=test-admin-token")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment; filename=signups.csv" in response.headers["content-disposition"]
    
    csv_content = response.text
    assert "Email,Name,License Key,Tier" in csv_content
    assert "customer@example.com" in csv_content

if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
