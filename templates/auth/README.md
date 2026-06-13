# Production-Ready Reusable Authentication Templates

This directory contains standardized, production-grade authentication boilerplates to boot-strap user/admin authentication in future startup projects.

## 1. Node.js (Express) Cookie-Based Authentication
A secure template utilizing signed HTTP-only cookies, JWT verification, and owner/admin level middleware gates.

### Implementation
```javascript
const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');

const app = express();
app.use(express.json());
app.use(cookieParser(process.env.COOKIE_SECRET)); // Use signed cookies

const JWT_SECRET = process.env.JWT_SECRET;
const COOKIE_OPTIONS = {
  httpOnly: true,
  secure: process.env.NODE_ENV === 'production',
  signed: true,
  sameSite: 'strict',
  maxAge: 24 * 60 * 60 * 1000 // 24 hours
};

// Authenticate Middleware
function authenticateToken(req, res, next) {
  const token = req.signedCookies.auth_token;
  if (!token) return res.status(401).json({ error: 'Access denied' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ error: 'Session expired' });
    req.user = user;
    next();
  });
}

// Role-based authorization middleware
function requireAdmin(req, res, next) {
  if (req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Admin permission required' });
  }
  next();
}

// Login route
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  // TODO: Validate user credentials from database here
  
  const token = jwt.sign({ email, role: 'admin' }, JWT_SECRET, { expiresIn: '24h' });
  res.cookie('auth_token', token, COOKIE_OPTIONS);
  return res.json({ success: true });
});

// Logout route
app.post('/api/logout', (req, res) => {
  res.clearCookie('auth_token');
  return res.json({ success: true });
});
```

---

## 2. Python (FastAPI) RS256 JWT Token Verification
A template for secure asymmetric (RS256) token validation, ideal for APIs, license verification, and microservices.

### Implementation
```python
import time
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
security = HTTPBearer()

# Standard RS256 verification public key PEM (load from config/env)
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"""

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # RS256 Asymmetric Cryptographic Verification
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        
        # Check expiration manually if not validated by library
        exp = payload.get("exp")
        if exp and exp < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@app.get("/api/secure-endpoint")
def secure_data(payload: dict = Depends(verify_jwt_token)):
    return {"message": "Access granted", "user": payload.get("sub")}
```
