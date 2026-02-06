# Research: Full-Stack Todo Web Application

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-08
**Status**: Complete

## Overview

This document captures research findings and technology decisions for implementing the Full-Stack Todo Web Application. All decisions align with the project constitution requirements.

---

## 1. Better Auth Integration with Next.js 16+ App Router

### Research Question
How to configure Better Auth in Next.js App Router (vs Pages Router) and determine optimal JWT token storage strategy?

### Decision: Better Auth with httpOnly Cookies

**Chosen Approach**:
- Use Better Auth library configured for Next.js 16+ App Router
- Store JWT tokens in httpOnly cookies (not localStorage)
- Implement auth callback route at `/app/auth/callback/page.tsx`
- Use Better Auth's built-in session management

**Rationale**:
- **httpOnly cookies** are more secure than localStorage (immune to XSS attacks)
- Better Auth provides native Next.js 16+ App Router support with server components
- Automatic token refresh handling built into Better Auth
- CSRF protection included with httpOnly cookies + SameSite attribute

**Alternatives Considered**:
1. **localStorage**: Rejected due to XSS vulnerability - any injected script can read tokens
2. **sessionStorage**: Rejected - tokens lost on tab close, poor UX
3. **Manual JWT handling**: Rejected - Better Auth provides battle-tested implementation

**Implementation Notes**:
- Configure Better Auth in `src/lib/auth.ts` with passwordless provider
- Set cookie options: `httpOnly: true, secure: true, sameSite: 'lax'`
- Frontend API client reads token from cookie automatically (sent with credentials: 'include')
- Backend validates token from Cookie header (fallback to Authorization header for API testing)

---

## 2. JWT Verification in FastAPI

### Research Question
Which JWT library to use (python-jose vs PyJWT) and how to implement verification (middleware vs dependency)?

### Decision: python-jose with Dependency Injection

**Chosen Approach**:
- Use `python-jose[cryptography]` for JWT validation
- Implement verification as FastAPI dependency (`get_current_user`)
- Extract user_id from JWT `sub` claim
- Validate token signature using BETTER_AUTH_SECRET

**Rationale**:
- **python-jose** is FastAPI's recommended JWT library (used in official docs)
- **Dependency injection** provides cleaner code than middleware - only applied to protected routes
- Easier to test and mock for unit tests
- Better error handling - can return specific 401 errors per endpoint

**Alternatives Considered**:
1. **PyJWT**: Rejected - python-jose has better FastAPI integration and documentation
2. **Middleware approach**: Rejected - applies to all routes including health checks; dependency injection more flexible

**Implementation Notes**:
```python
# src/api/dependencies.py
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)) -> str:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Token Claims Structure**:
- `sub`: user_id (primary identifier)
- `exp`: expiration timestamp (24 hours from issue)
- `iat`: issued at timestamp

---

## 3. Neon PostgreSQL Connection Patterns

### Research Question
How to configure connection pooling with Neon Serverless and whether to use async or sync database operations?

### Decision: Synchronous SQLModel with Connection Pooling

**Chosen Approach**:
- Use synchronous SQLModel (not async) for simplicity
- Configure connection pooling via SQLAlchemy engine
- Use `psycopg2-binary` driver (not psycopg3)
- Connection string includes `sslmode=require` and `channel_binding=require`

**Rationale**:
- **Synchronous operations** are simpler for CRUD operations (no async/await complexity)
- Neon's connection pooler handles concurrency at database level
- SQLModel's sync API is more mature and better documented
- Performance adequate for 100 concurrent users (per requirements)

**Alternatives Considered**:
1. **Async SQLModel**: Rejected - adds complexity without significant benefit for this use case
2. **Raw psycopg2**: Rejected - SQLModel provides ORM benefits (validation, relationships)
3. **SQLAlchemy directly**: Rejected - SQLModel provides Pydantic integration

**Implementation Notes**:
```python
# src/database.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
# Neon connection string format:
# postgresql://user:pass@host/db?sslmode=require&channel_binding=require

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set True for SQL logging in development
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Max connections beyond pool_size
    pool_pre_ping=True,  # Verify connections before use
)

def get_session():
    with Session(engine) as session:
        yield session
```

**Connection Pool Configuration**:
- `pool_size=5`: Base connections (adequate for 100 users with fast queries)
- `max_overflow=10`: Burst capacity for traffic spikes
- `pool_pre_ping=True`: Handles Neon's serverless connection recycling

---

## 4. User Ownership Enforcement Patterns

### Research Question
How to enforce user ownership at query level to prevent cross-user data access?

### Decision: Query Filtering with Path Parameter Validation

**Chosen Approach**:
- Validate `user_id` in URL path matches JWT `sub` claim
- Filter all database queries by `user_id` at ORM level
- Return 403 Forbidden if user_id mismatch
- Return 404 Not Found if task doesn't exist OR doesn't belong to user (prevents information leakage)

**Rationale**:
- **Path parameter validation** provides explicit security check before database query
- **ORM-level filtering** prevents accidental queries without user_id filter
- **404 for unauthorized access** prevents attackers from discovering which task IDs exist
- Defense in depth: validation at API layer + filtering at database layer

**Alternatives Considered**:
1. **Application-level filtering only**: Rejected - easy to forget filter in new endpoints
2. **Database row-level security**: Rejected - adds complexity, Neon may not support
3. **Separate user_id from path**: Rejected - constitution requires `/api/{user_id}/tasks` format

**Implementation Pattern**:
```python
# src/api/routes/tasks.py
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Validate user_id matches JWT
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access forbidden")

    # Query with user_id filter
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks

@router.get("/api/{user_id}/tasks/{task_id}")
async def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Access forbidden")

    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()

    if not task:
        # Return 404 whether task doesn't exist or belongs to another user
        raise HTTPException(status_code=404, detail="Task not found")

    return task
```

**Security Considerations**:
- Always validate `user_id` parameter against JWT before any database operation
- Use parameterized queries (SQLModel handles this) to prevent SQL injection
- Return generic 404 for unauthorized access to prevent task ID enumeration

---

## 5. CORS Configuration

### Research Question
How to configure CORS for frontend-backend communication in development and production?

### Decision: FastAPI CORS Middleware with Environment-Based Origins

**Chosen Approach**:
- Use FastAPI's `CORSMiddleware`
- Allow origins from environment variable `ALLOWED_ORIGINS`
- Development: `http://localhost:3000` (Next.js default)
- Production: Actual frontend domain
- Allow credentials for httpOnly cookie transmission

**Rationale**:
- **Environment-based configuration** supports different origins per environment
- **Allow credentials** required for httpOnly cookies to be sent cross-origin
- FastAPI's built-in middleware handles preflight requests automatically

**Alternatives Considered**:
1. **Allow all origins (*)**: Rejected - security risk, doesn't work with credentials
2. **Hardcoded origins**: Rejected - inflexible for different environments
3. **No CORS (same-origin only)**: Rejected - requires frontend and backend on same domain

**Implementation Notes**:
```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Frontend URLs
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Environment Variables**:
- Development: `ALLOWED_ORIGINS=http://localhost:3000`
- Production: `ALLOWED_ORIGINS=https://yourdomain.com`
- Multiple origins: `ALLOWED_ORIGINS=https://app.com,https://admin.app.com`

---

## Additional Technology Decisions

### Database Migrations

**Decision**: Use Alembic for database migrations

**Rationale**:
- SQLModel is built on SQLAlchemy, which integrates with Alembic
- Alembic provides version control for database schema
- Essential for production deployments and schema evolution

**Implementation**:
- Initialize Alembic in backend directory
- Create initial migration for User and Task tables
- Run migrations as part of deployment process

### Error Handling

**Decision**: Standardized error response format

**Format**:
```json
{
  "detail": "Human-readable error message",
  "error_code": "TASK_NOT_FOUND",
  "status_code": 404
}
```

**Rationale**:
- Consistent error format simplifies frontend error handling
- Error codes enable internationalization
- Status codes follow HTTP standards

### Frontend API Client

**Decision**: Custom fetch wrapper with automatic JWT attachment

**Implementation**:
```typescript
// src/lib/api.ts
async function apiClient(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`http://localhost:8001${endpoint}`, {
    ...options,
    credentials: 'include',  // Send httpOnly cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}
```

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| JWT Storage | httpOnly cookies | XSS protection, automatic transmission |
| JWT Library | python-jose | FastAPI recommended, good documentation |
| Auth Pattern | Dependency injection | Flexible, testable, clean code |
| Database | Sync SQLModel | Simpler than async, adequate performance |
| Connection Pool | 5 base + 10 overflow | Handles 100 concurrent users |
| Ownership Enforcement | Path validation + query filtering | Defense in depth, prevents leakage |
| CORS | Environment-based origins | Flexible, secure, supports credentials |
| Migrations | Alembic | Industry standard, SQLAlchemy integration |

---

## Risks and Mitigations

1. **Better Auth Learning Curve**
   - Risk: Team unfamiliar with Better Auth
   - Mitigation: Follow official Next.js 16+ examples, allocate extra time for auth implementation

2. **Neon Connection Limits**
   - Risk: Serverless PostgreSQL may throttle connections
   - Mitigation: Connection pooling configured, monitor connection usage

3. **CORS Issues in Production**
   - Risk: Misconfigured CORS blocks frontend
   - Mitigation: Test CORS in staging environment before production deployment

---

## Next Steps

1. Create `data-model.md` with detailed User and Task entity definitions
2. Create `contracts/api-spec.yaml` with OpenAPI specification for all 6 endpoints
3. Create `quickstart.md` with step-by-step setup instructions
4. Validate all decisions against constitution requirements
