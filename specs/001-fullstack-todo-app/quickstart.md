# Quickstart Guide: Full-Stack Todo Web Application

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-08
**Status**: Complete

## Overview

This guide provides step-by-step instructions to set up and run the Full-Stack Todo Web Application locally. Follow these instructions to get the backend API and frontend UI running on your development machine.

---

## Prerequisites

Before starting, ensure you have the following installed:

### Required Software

- **Python 3.11+** - Backend runtime
  - Check: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- **Node.js 20+** - Frontend runtime
  - Check: `node --version`
  - Download: https://nodejs.org/

- **npm or yarn** - Package manager
  - Check: `npm --version` or `yarn --version`
  - Included with Node.js

- **Git** - Version control
  - Check: `git --version`
  - Download: https://git-scm.com/

### Required Accounts

- **Neon PostgreSQL Account** - Database hosting
  - Sign up: https://neon.tech/
  - Database connection string provided in constitution

- **Better Auth Account** (if required) - Authentication service
  - Check Better Auth documentation for setup requirements

---

## Project Structure

```text
Phase-2/
├── backend/              # FastAPI backend
│   ├── src/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
├── frontend/             # Next.js frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── .env.local
├── specs/                # Feature specifications
└── README.md
```

---

## Part 1: Environment Setup

### 1.1 Clone Repository

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd Phase-2

# Checkout the feature branch
git checkout 001-fullstack-todo-app
```

### 1.2 Configure Environment Variables

#### Backend Environment Variables

Create `backend/.env` file:

```bash
# Navigate to backend directory
cd backend

# Create .env file
touch .env  # On Windows: type nul > .env
```

Add the following content to `backend/.env`:

```env
# Database Configuration
DATABASE_URL=postgresql://neondb_owner:npg_LG7oZUwzO2Pk@ep-silent-morning-adwt0kau-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Authentication Configuration
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000

# Application Configuration
PORT=8001
DEBUG=True
```

**⚠️ Security Notes**:
- Never commit `.env` files to version control
- Change `BETTER_AUTH_SECRET` to a strong random value in production
- Use different secrets for development and production

#### Frontend Environment Variables

Create `frontend/.env.local` file:

```bash
# Navigate to frontend directory
cd ../frontend

# Create .env.local file
touch .env.local  # On Windows: type nul > .env.local
```

Add the following content to `frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8001

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
BETTER_AUTH_URL=http://localhost:3000

# Better Auth Provider Configuration (adjust based on Better Auth setup)
BETTER_AUTH_PROVIDER=email
```

**⚠️ Security Notes**:
- `NEXT_PUBLIC_*` variables are exposed to the browser
- Never put secrets in `NEXT_PUBLIC_*` variables
- `.env.local` is gitignored by default in Next.js

---

## Part 2: Backend Setup

### 2.1 Install Python Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected dependencies** (from `requirements.txt`):
```text
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
pydantic==2.5.3
alembic==1.13.1
pytest==7.4.4
httpx==0.26.0
```

### 2.2 Initialize Database

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Run migrations
alembic upgrade head
```

**Verify database connection**:
```bash
# Test database connection
python -c "from src.database import engine; print('Database connected successfully!')"
```

### 2.3 Start Backend Server

```bash
# Start FastAPI server on port 8001
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Verify backend is running**:
- Open browser: http://localhost:8001/docs
- You should see the FastAPI Swagger UI with API documentation

---

## Part 3: Frontend Setup

### 3.1 Install Node Dependencies

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install
# Or with yarn:
# yarn install
```

**Expected dependencies** (from `package.json`):
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "better-auth": "^latest",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0"
  }
}
```

### 3.2 Configure Better Auth

Create `frontend/src/lib/auth.ts`:

```typescript
import { createAuth } from 'better-auth';

export const auth = createAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,
  providers: {
    email: {
      enabled: true,
      // Configure email provider settings
    },
  },
});
```

### 3.3 Start Frontend Development Server

```bash
# Start Next.js development server
npm run dev
# Or with yarn:
# yarn dev

# Expected output:
# ▲ Next.js 16.0.0
# - Local:        http://localhost:3000
# - Ready in 2.3s
```

**Verify frontend is running**:
- Open browser: http://localhost:3000
- You should see the landing/login page

---

## Part 4: Validation & Testing

### 4.1 Test Backend API

#### Test Health Check (if implemented)
```bash
curl http://localhost:8001/health
# Expected: {"status": "healthy"}
```

#### Test Authentication (requires JWT token)
```bash
# This will fail without authentication (expected)
curl http://localhost:8001/api/550e8400-e29b-41d4-a716-446655440000/tasks
# Expected: {"detail": "Not authenticated"}
```

### 4.2 Test Frontend Authentication Flow

1. **Open frontend**: http://localhost:3000
2. **Click login/signup**: Enter your email address
3. **Check email**: Look for magic link from Better Auth
4. **Click magic link**: Should redirect to authenticated state
5. **Verify redirect**: Should see task list page (empty for new users)

### 4.3 Test Task CRUD Operations

#### Create a Task
1. Navigate to task list page (after authentication)
2. Enter task title: "Test task"
3. Enter description (optional): "This is a test"
4. Click "Create" or "Add Task"
5. **Verify**: Task appears in the list immediately

#### View Tasks
1. Refresh the page
2. **Verify**: Task persists and is still visible

#### Edit a Task
1. Click "Edit" on the test task
2. Change title to: "Updated test task"
3. Click "Save"
4. **Verify**: Task title updates immediately

#### Complete a Task
1. Click checkbox or "Complete" button on the task
2. **Verify**: Task shows completion indicator (strikethrough, checkmark, etc.)
3. Click again to mark incomplete
4. **Verify**: Task returns to active state

#### Delete a Task
1. Click "Delete" on the test task
2. Confirm deletion (if confirmation dialog shown)
3. **Verify**: Task disappears from the list
4. Refresh page
5. **Verify**: Task does not reappear

### 4.4 Test User Isolation

**Important Security Test**:

1. **Create tasks as User A**:
   - Authenticate as user A (email: usera@example.com)
   - Create 2-3 tasks
   - Note the user_id from JWT token (check browser dev tools)

2. **Authenticate as User B**:
   - Log out from User A
   - Authenticate as user B (email: userb@example.com)
   - **Verify**: User B sees an empty task list (no User A tasks)

3. **Attempt cross-user access** (API testing):
   ```bash
   # Get User B's JWT token from browser dev tools
   # Try to access User A's tasks with User B's token
   curl -H "Authorization: Bearer <user-b-token>" \
        http://localhost:8001/api/<user-a-id>/tasks

   # Expected: 403 Forbidden
   ```

4. **Verify isolation**:
   - User A can only see User A's tasks
   - User B can only see User B's tasks
   - No cross-user data leakage

---

## Part 5: Running Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v
```

**Expected test categories**:
- Authentication tests (JWT validation)
- Task CRUD tests (create, read, update, delete)
- User ownership tests (cross-user access prevention)
- Validation tests (empty title, character limits)

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run all tests
npm test
# Or with yarn:
# yarn test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

**Expected test categories**:
- Component tests (TaskList, TaskItem, TaskForm)
- Authentication flow tests
- API client tests

---

## Part 6: Common Issues & Troubleshooting

### Issue 1: Database Connection Failed

**Symptoms**:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solutions**:
1. Verify `DATABASE_URL` in `backend/.env` is correct
2. Check Neon PostgreSQL dashboard - database may be paused
3. Verify SSL mode is set: `sslmode=require`
4. Test connection: `psql $DATABASE_URL`

### Issue 2: Port 8001 Already in Use

**Symptoms**:
```
ERROR: [Errno 48] Address already in use
```

**Solutions**:
1. Find process using port 8001:
   ```bash
   # On macOS/Linux:
   lsof -i :8001
   # On Windows:
   netstat -ano | findstr :8001
   ```
2. Kill the process or use a different port (update `.env` and frontend API URL)

### Issue 3: CORS Errors in Browser

**Symptoms**:
```
Access to fetch at 'http://localhost:8001' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solutions**:
1. Verify `ALLOWED_ORIGINS` in `backend/.env` includes `http://localhost:3000`
2. Restart backend server after changing `.env`
3. Check browser console for specific CORS error details

### Issue 4: JWT Token Not Sent with Requests

**Symptoms**:
- API returns 401 Unauthorized
- Token exists in browser but not sent with requests

**Solutions**:
1. Verify `credentials: 'include'` in fetch requests
2. Check cookie settings (httpOnly, sameSite)
3. Verify CORS allows credentials (`allow_credentials=True`)
4. Check browser dev tools → Network → Request Headers

### Issue 5: Better Auth Configuration Issues

**Symptoms**:
- Authentication flow fails
- Magic link not received
- Callback errors

**Solutions**:
1. Verify `BETTER_AUTH_SECRET` matches between frontend and backend
2. Check Better Auth provider configuration
3. Verify email provider settings (SMTP, API keys)
4. Check Better Auth logs for detailed error messages

### Issue 6: Alembic Migration Errors

**Symptoms**:
```
alembic.util.exc.CommandError: Target database is not up to date
```

**Solutions**:
1. Check current migration version: `alembic current`
2. View migration history: `alembic history`
3. Upgrade to latest: `alembic upgrade head`
4. If stuck, downgrade and re-upgrade: `alembic downgrade -1 && alembic upgrade head`

---

## Part 7: Development Workflow

### Daily Development Routine

1. **Start backend**:
   ```bash
   cd backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   uvicorn src.main:app --reload --port 8001
   ```

2. **Start frontend** (in new terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Make changes**: Edit code in `backend/src/` or `frontend/src/`

4. **Test changes**: Both servers auto-reload on file changes

5. **Run tests**: Before committing changes
   ```bash
   # Backend tests
   cd backend && pytest

   # Frontend tests
   cd frontend && npm test
   ```

### Code Quality Checks

```bash
# Backend linting (if configured)
cd backend
flake8 src/
black src/ --check
mypy src/

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

---

## Part 8: Next Steps

After completing this quickstart:

1. **Review Specifications**:
   - Read `specs/001-fullstack-todo-app/spec.md` for requirements
   - Review `specs/001-fullstack-todo-app/plan.md` for architecture

2. **Implement Features**:
   - Run `/sp.tasks` to generate detailed task breakdown
   - Follow task list for systematic implementation

3. **Deploy to Production**:
   - Update environment variables for production
   - Configure production database
   - Set up CI/CD pipeline
   - Deploy backend and frontend separately

4. **Monitor & Maintain**:
   - Set up logging and monitoring
   - Monitor database performance
   - Track API error rates
   - Collect user feedback

---

## Part 9: Useful Commands Reference

### Backend Commands

```bash
# Start server
uvicorn src.main:app --reload --port 8001

# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check database connection
python -c "from src.database import engine; print('Connected!')"
```

### Frontend Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Run linter
npm run lint

# Type check
npm run type-check
```

### Database Commands

```bash
# Connect to Neon PostgreSQL
psql $DATABASE_URL

# List tables
\dt

# Describe table
\d tasks

# Query tasks
SELECT * FROM tasks LIMIT 10;

# Count tasks by user
SELECT user_id, COUNT(*) FROM tasks GROUP BY user_id;
```

---

## Part 10: Support & Resources

### Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Better Auth**: https://better-auth.com/docs
- **Neon PostgreSQL**: https://neon.tech/docs

### API Documentation

- **Swagger UI**: http://localhost:8001/docs (when backend running)
- **ReDoc**: http://localhost:8001/redoc (alternative API docs)
- **OpenAPI Spec**: `specs/001-fullstack-todo-app/contracts/api-spec.yaml`

### Getting Help

1. Check this quickstart guide first
2. Review troubleshooting section
3. Check API documentation at `/docs`
4. Review specification documents in `specs/`
5. Check project README.md

---

## Summary

You should now have:
- ✅ Backend API running on http://localhost:8001
- ✅ Frontend UI running on http://localhost:3000
- ✅ Database connected to Neon PostgreSQL
- ✅ Authentication working with Better Auth
- ✅ Task CRUD operations functional
- ✅ User isolation verified

**Next**: Run `/sp.tasks` to generate detailed implementation tasks and begin development!
