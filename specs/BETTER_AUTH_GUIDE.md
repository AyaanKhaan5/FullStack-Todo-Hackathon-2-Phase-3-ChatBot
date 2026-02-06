# Better Auth Integration Guide

**Status**: 🔴 Critical - Required for Working MVP
**Estimated Time**: 1-2 hours
**Priority**: Highest

---

## Overview

Better Auth is a passwordless authentication library that needs to be configured to enable user login and JWT token generation. This is the **only remaining blocker** for a working MVP.

---

## Current State

### ✅ What's Already Done
- Backend JWT verification middleware (`backend/src/middleware/auth.py`)
- Frontend auth placeholder (`frontend/src/lib/auth.ts`)
- API client configured for credentials: 'include' (`frontend/src/lib/api.ts`)
- Environment variables set up (BETTER_AUTH_SECRET in both .env files)
- Protected route layout (`frontend/src/app/tasks/layout.tsx`)
- Auth callback page (`frontend/src/app/auth/callback/page.tsx`)

### ❌ What's Missing
- Better Auth client initialization
- Email provider configuration (e.g., Resend, SendGrid)
- Login UI implementation
- Session management
- User context provider
- JWT token generation/validation alignment

---

## Implementation Steps

### Step 1: Research Better Auth Documentation

**Action**: Visit Better Auth documentation to understand the latest setup for Next.js 16+

**Key Questions to Answer**:
1. What's the correct way to initialize Better Auth client in Next.js 16 App Router?
2. Which email provider is recommended (Resend, SendGrid, etc.)?
3. How does Better Auth generate JWT tokens?
4. What's the token format and claims structure?
5. How to set up server-side session management?

**Resources**:
- Better Auth official documentation
- Next.js 16 App Router authentication patterns
- Better Auth GitHub repository examples

### Step 2: Choose and Configure Email Provider

**Recommended**: Resend (modern, developer-friendly, generous free tier)

**Alternative Options**:
- SendGrid
- AWS SES
- Mailgun
- Postmark

**Configuration Needed**:
1. Sign up for email provider account
2. Get API key
3. Verify sender domain (or use sandbox for testing)
4. Add API key to `.env` and `.env.local`

**Environment Variables to Add**:
```env
# Backend (.env)
EMAIL_PROVIDER=resend
EMAIL_API_KEY=re_xxxxxxxxxxxxx
EMAIL_FROM=noreply@yourdomain.com

# Frontend (.env.local)
NEXT_PUBLIC_EMAIL_PROVIDER=resend
```

### Step 3: Install Better Auth (if not already installed)

**Check Current Installation**:
```bash
cd frontend
npm list better-auth
```

**If Not Installed or Outdated**:
```bash
npm install better-auth@latest
npm install @better-auth/react  # If using React hooks
```

### Step 4: Configure Better Auth Client

**File**: `frontend/src/lib/auth.ts`

**Implementation Pattern**:
```typescript
import { createAuthClient } from 'better-auth/client';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
  // OR if Better Auth runs on frontend:
  // baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3000',

  credentials: 'include', // Important for httpOnly cookies

  providers: {
    email: {
      enabled: true,
      // Email provider config
    },
  },
});

// Export auth functions
export const signIn = authClient.signIn;
export const signOut = authClient.signOut;
export const getSession = authClient.getSession;
```

**Key Decisions**:
1. **Where does Better Auth run?**
   - Option A: On backend (FastAPI) - requires Better Auth Python integration
   - Option B: On frontend (Next.js API routes) - easier for Next.js
   - **Recommendation**: Option B (Next.js API routes)

2. **Token Storage**:
   - Use httpOnly cookies (already configured in API client)
   - Never store tokens in localStorage (XSS vulnerability)

### Step 5: Create Better Auth API Routes (Next.js)

**File**: `frontend/src/app/api/auth/[...auth]/route.ts`

**Implementation Pattern**:
```typescript
import { createAuthHandler } from 'better-auth/next';
import { authConfig } from '@/lib/auth';

const handler = createAuthHandler(authConfig);

export { handler as GET, handler as POST };
```

**This creates endpoints**:
- `POST /api/auth/signin` - Send magic link
- `GET /api/auth/callback` - Verify magic link
- `POST /api/auth/signout` - Sign out
- `GET /api/auth/session` - Get current session

### Step 6: Implement Login UI

**File**: `frontend/src/app/page.tsx`

**Implementation Pattern**:
```typescript
'use client';

import { useState } from 'react';
import { signIn } from '@/lib/auth';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signIn({ email });
      setSent(true);
    } catch (error) {
      console.error('Sign in error:', error);
      alert('Failed to send magic link');
    } finally {
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2>Check your email</h2>
          <p>We sent a magic link to {email}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <h1>Sign In</h1>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Sending...' : 'Send Magic Link'}
        </button>
      </form>
    </div>
  );
}
```

### Step 7: Create Auth Context Provider

**File**: `frontend/src/contexts/AuthContext.tsx`

**Implementation Pattern**:
```typescript
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { getSession } from '@/lib/auth';

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadSession() {
      try {
        const session = await getSession();
        setUser(session?.user || null);
      } catch (error) {
        console.error('Failed to load session:', error);
      } finally {
        setLoading(false);
      }
    }

    loadSession();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

**Update Root Layout**: `frontend/src/app/layout.tsx`
```typescript
import { AuthProvider } from '@/contexts/AuthContext';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

### Step 8: Update Tasks Page to Use Auth Context

**File**: `frontend/src/app/tasks/page.tsx`

**Changes**:
```typescript
import { useAuth } from '@/contexts/AuthContext';

export default function TasksPage() {
  const { user, loading: authLoading } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTasks() {
      if (!user) return; // Wait for auth

      try {
        setLoading(true);
        const fetchedTasks = await taskApi.list(user.id); // Use real user ID
        setTasks(fetchedTasks);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTasks();
  }, [user]);

  if (authLoading) {
    return <div>Loading authentication...</div>;
  }

  if (!user) {
    redirect('/'); // Redirect to login
  }

  // Rest of component...
}
```

### Step 9: Align Backend JWT Verification

**File**: `backend/src/middleware/auth.py`

**Current Implementation**:
```python
def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        # ...
```

**Verify**:
1. Better Auth uses HS256 algorithm ✅
2. User ID is in "sub" claim ✅
3. Secret matches between frontend and backend ✅

**If Better Auth uses different format**:
- Check Better Auth documentation for JWT structure
- Update `verify_jwt_token` to match Better Auth's token format
- May need to verify issuer, audience, etc.

### Step 10: Test Authentication Flow

**Test Checklist**:
1. ✅ User can enter email on login page
2. ✅ Magic link email is sent
3. ✅ User clicks magic link
4. ✅ User is redirected to /auth/callback
5. ✅ JWT token is set in httpOnly cookie
6. ✅ User is redirected to /tasks
7. ✅ Tasks page fetches user's tasks
8. ✅ Backend verifies JWT token
9. ✅ User sees their tasks
10. ✅ User can sign out

**Testing Commands**:
```bash
# Check if JWT cookie is set
# In browser DevTools > Application > Cookies

# Test backend JWT verification
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8001/api/USER_ID/tasks

# Check backend logs for JWT verification
# Should see: "User authenticated: USER_ID"
```

---

## Common Issues and Solutions

### Issue 1: CORS Errors
**Symptom**: "CORS policy: No 'Access-Control-Allow-Origin' header"
**Solution**: Verify CORS configuration in `backend/src/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,  # Important!
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### Issue 2: JWT Token Not Sent
**Symptom**: Backend returns 401 Unauthorized
**Solution**: Ensure `credentials: 'include'` in API client:
```typescript
const config: RequestInit = {
  credentials: 'include', // This line is critical
  // ...
};
```

### Issue 3: Email Not Sending
**Symptom**: Magic link email never arrives
**Solutions**:
1. Check email provider API key is correct
2. Verify sender email is verified with provider
3. Check spam folder
4. Look at email provider dashboard for delivery logs
5. Use sandbox mode for testing (if available)

### Issue 4: JWT Secret Mismatch
**Symptom**: Backend rejects valid tokens
**Solution**: Ensure BETTER_AUTH_SECRET is identical in:
- `backend/.env`
- `frontend/.env.local`
- Better Auth configuration

### Issue 5: Token Expiration
**Symptom**: User logged out unexpectedly
**Solution**: Configure token expiration in Better Auth:
```typescript
export const authConfig = {
  session: {
    expiresIn: '7d', // 7 days
    updateAge: '1d', // Refresh token daily
  },
};
```

---

## Alternative: Simplified Testing Without Email

For **testing purposes only**, you can bypass email and manually create JWT tokens:

### Backend: Create Test Endpoint

**File**: `backend/src/api/routes/auth.py` (NEW FILE)
```python
from fastapi import APIRouter
from jose import jwt
from datetime import datetime, timedelta
from ..config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/test-token")
async def create_test_token(email: str):
    """TESTING ONLY - Create JWT token without email verification"""
    user_id = "test-user-123"  # In production, create real user

    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }

    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    return {
        "token": token,
        "user_id": user_id,
        "email": email
    }
```

**Register in main.py**:
```python
from .api.routes import auth
app.include_router(auth.router)
```

### Frontend: Manual Token Setting

**For testing**, manually set token in browser console:
```javascript
// Get token from backend
fetch('http://localhost:8001/api/auth/test-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'test@example.com' })
})
.then(r => r.json())
.then(data => {
  console.log('Token:', data.token);
  // Manually set in Authorization header for testing
});
```

**⚠️ WARNING**: Remove test endpoint before production!

---

## Recommended Approach

### For Quick Testing (30 minutes)
1. Use test token endpoint (above)
2. Manually set Authorization header
3. Test task CRUD operations
4. Verify user ownership enforcement

### For Production MVP (1-2 hours)
1. Set up Resend account (free tier)
2. Configure Better Auth with Resend
3. Implement full authentication flow
4. Test end-to-end with real email

---

## Success Criteria

✅ **Authentication Working When**:
1. User can sign in with email
2. Magic link email is received
3. User is authenticated after clicking link
4. JWT token is stored in httpOnly cookie
5. Backend accepts JWT token
6. User can fetch their tasks
7. User ownership is enforced
8. User can sign out

---

## Next Steps After Auth

Once authentication is working:

1. **Test Task Creation** (Phase 4)
   - Create task form
   - Test POST endpoint

2. **Test Task Editing** (Phase 5)
   - Edit task inline
   - Test PUT endpoint

3. **Test Task Deletion** (Phase 5)
   - Delete confirmation
   - Test DELETE endpoint

4. **Test Task Completion** (Phase 6)
   - Toggle checkbox
   - Test PATCH endpoint

5. **Security Testing** (Phase 7)
   - Test unauthorized access
   - Test cross-user access prevention

---

## Resources

### Documentation
- Better Auth: https://better-auth.com/docs
- Next.js Authentication: https://nextjs.org/docs/app/building-your-application/authentication
- Resend: https://resend.com/docs

### Example Repositories
- Search GitHub for "better-auth nextjs 16 example"
- Look for official Better Auth examples

### Email Providers
- Resend: https://resend.com (Recommended)
- SendGrid: https://sendgrid.com
- AWS SES: https://aws.amazon.com/ses

---

## Estimated Time Breakdown

| Task | Time | Priority |
|------|------|----------|
| Research Better Auth docs | 15 min | High |
| Set up email provider | 15 min | High |
| Configure Better Auth client | 20 min | High |
| Implement login UI | 20 min | High |
| Create auth context | 15 min | High |
| Update tasks page | 10 min | High |
| Test authentication flow | 20 min | High |
| Debug issues | 20 min | Medium |
| **Total** | **2 hours** | - |

---

**Status**: Ready for implementation
**Blocker**: None (all prerequisites complete)
**Next Action**: Research Better Auth documentation and choose email provider
