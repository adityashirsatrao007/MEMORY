# Clerk Authentication — Free Pro Plan

## When to Use
- Any project needs user auth
- SaaS applications
- Multi-tenant systems

## Quick Setup
```bash
# Claim at: https://clerk.com/education
# Get keys from dashboard

# Save keys
echo "CLERK_PUBLISHABLE_KEY=pk_test_xxx" >> ~/.config/global-apikeys/keys.env
echo "CLERK_SECRET_KEY=sk_test_xxx" >> ~/.config/global-apikeys/keys.env
```

## React Integration
```jsx
import { ClerkProvider, SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/clerk-react';

function App() {
  return (
    <ClerkProvider publishableKey={process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY}>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </ClerkProvider>
  );
}
```

## Next.js Integration
```jsx
// app/layout.tsx
import { ClerkProvider } from '@clerk/nextjs'

export default function Layout({ children }) {
  return (
    <ClerkProvider>
      {children}
    </ClerkProvider>
  )
}

// app/page.tsx
import { auth } from '@clerk/nextjs/server'

export default async function Home() {
  const { userId } = await auth()
  return userId ? <Dashboard /> : <SignInButton />
}
```

## Backend Protection
```python
# FastAPI middleware
from clerk_backend_api import Clerk

clerk = Clerk(bearer_auth=os.environ['CLERK_SECRET_KEY'])

@app.middleware("http")
async def auth_middleware(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return JSONResponse(status_code=401, content={"error": "No token"})
    try:
        user = clrek.users.verify(token)
        request.state.user = user
    except Exception:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    return await call_next(request)
```

## Webhooks
```python
# Handle user events
@app.post("/webhooks/clerk")
async def clerk_webhook(request: Request):
    data = await request.json()
    if data["type"] == "user.created":
        # Create user in your DB
        pass
    elif data["type"] == "user.deleted":
        # Cleanup
        pass
    return {"status": "ok"}
```

## Features Included (Free)
- Unlimited users
- Social logins (Google, GitHub, etc.)
- Multi-factor auth
- Session management
- Webhooks
- User management dashboard

## Student Benefits
- Free Pro plan while student
- No credit card needed
- Production-ready auth in minutes
