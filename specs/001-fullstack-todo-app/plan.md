# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `001-fullstack-todo-app` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fullstack-todo-app/spec.md`

## Summary

Transform the console-based Todo application into a modern, multi-user, authenticated full-stack web application with persistent storage. The system will provide passwordless authentication using Better Auth with JWT tokens, a FastAPI backend running on port 8001 with user ownership enforcement, and a Next.js 16+ frontend with responsive UI. All task data will be persisted to Neon Serverless PostgreSQL using SQLModel ORM, with strict user isolation ensuring each user can only access their own tasks.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Node.js 20+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.109+, SQLModel 0.0.14+, python-jose[cryptography] (JWT), psycopg2-binary (PostgreSQL driver)
- Frontend: Next.js 16+, Better Auth, React 19+, Tailwind CSS 3+, TypeScript 5+

**Storage**: Neon Serverless PostgreSQL (cloud-hosted, connection pooling enabled)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge), Linux/Windows server for backend
**Project Type**: Web application (monorepo with separate backend and frontend)
**Performance Goals**:
- API response time <200ms p95 for CRUD operations
- Authentication flow completion <30 seconds
- Task list rendering <1 second for up to 1000 tasks
- Support 100+ concurrent authenticated users

**Constraints**:
- Backend MUST run on port 8001 only
- Database MUST use provided Neon connection string via DATABASE_URL
- All API routes MUST enforce user ownership (user_id in URL matches JWT user_id)
- No hardcoded credentials permitted
- Frontend MUST use Next.js App Router (not Pages Router)

**Scale/Scope**:
- Initial deployment: 10-50 users
- Task volume: Up to 10,000 tasks per user
- 6 REST API endpoints
- 4 user stories (P1-P4)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Technology Stack Compliance ✅

- ✅ **Backend**: Python with FastAPI (compliant)
- ✅ **Backend Port**: 8001 only (compliant)
- ✅ **Database**: Neon Serverless PostgreSQL (compliant)
- ✅ **ORM**: SQLModel (compliant)
- ✅ **Authentication**: Better Auth with JWT (compliant)
- ✅ **Frontend**: Next.js 16+ with App Router (compliant)

### Security & Authentication Compliance ✅

- ✅ **Passwordless Auth**: Better Auth configured for magic link/email authentication
- ✅ **JWT Tokens**: All API requests require Bearer token in Authorization header
- ✅ **User Ownership**: All endpoints validate user_id in URL matches JWT user_id
- ✅ **Environment Variables**: DATABASE_URL, BETTER_AUTH_SECRET stored in .env files
- ✅ **No Hardcoded Credentials**: All secrets loaded from environment

### Architecture & Structure Compliance ✅

- ✅ **Monorepo**: Backend and frontend as separate modules in single repository
- ✅ **Spec-Kit Plus Compatible**: Follows /specs directory structure
- ✅ **Specification Authority**: Implementation follows spec.md requirements

### Development Workflow Compliance ✅

- ✅ **Spec-First**: Plan created after specification approval
- ✅ **Small Changes**: Implementation broken into phases and tasks
- ✅ **Traceability**: All requirements mapped to functional requirements (FR-001 through FR-033)

**GATE STATUS**: ✅ PASSED - All constitution requirements satisfied, no violations to justify

## Project Structure

### Documentation (this feature)

```text
specs/001-fullstack-todo-app/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── api-spec.yaml    # OpenAPI 3.0 specification
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Monorepo structure for web application
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLModel
│   │   └── task.py          # Task SQLModel
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py          # JWT verification middleware
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py  # Dependency injection (get_current_user, get_db)
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── tasks.py     # Task CRUD endpoints
│   └── schemas/
│       ├── __init__.py
│       ├── task.py          # Pydantic request/response schemas
│       └── user.py          # User schemas
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Authentication tests
│   └── test_tasks.py        # Task CRUD tests
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md                # Backend setup instructions

frontend/
├── src/
│   ├── app/                 # Next.js App Router
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Landing/login page
│   │   ├── auth/
│   │   │   └── callback/
│   │   │       └── page.tsx # Auth callback handler
│   │   └── tasks/
│   │       ├── page.tsx     # Task list page
│   │       └── layout.tsx   # Protected layout
│   ├── components/
│   │   ├── TaskList.tsx     # Task list component
│   │   ├── TaskItem.tsx     # Individual task component
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   └── AuthProvider.tsx # Better Auth context provider
│   ├── lib/
│   │   ├── api.ts           # API client with JWT attachment
│   │   ├── auth.ts          # Better Auth configuration
│   │   └── types.ts         # TypeScript type definitions
│   └── styles/
│       └── globals.css      # Tailwind CSS imports
├── public/
│   └── favicon.ico
├── tests/
│   └── components/
│       └── TaskList.test.tsx
├── .env.local.example       # Environment variable template
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md                # Frontend setup instructions

# Root level
.env                         # Environment variables (gitignored)
.gitignore
README.md                    # Monorepo overview and setup
package.json                 # Root package.json for workspace management
```

**Structure Decision**: Selected Option 2 (Web application) with monorepo structure. Backend and frontend are separate modules with independent dependency management but coordinated development. This structure:
- Enables independent deployment of backend and frontend
- Supports clear separation of concerns (API vs UI)
- Facilitates parallel development of backend and frontend features
- Aligns with Spec-Kit Plus conventions for web applications
- Allows shared TypeScript types between frontend and backend (future enhancement)

## Complexity Tracking

> **No violations detected** - Constitution Check passed all requirements. This section is empty as no complexity justification is needed.

---

## Phase 0: Research & Technology Validation

**Objective**: Resolve technical unknowns and validate technology integration patterns before detailed design.

### Research Tasks

1. **Better Auth Integration with Next.js 16+ App Router**
   - Research: How to configure Better Auth in Next.js App Router (vs Pages Router)
   - Research: JWT token storage best practices (httpOnly cookies vs localStorage)
   - Research: Auth callback handling in App Router
   - Decision needed: Token storage mechanism
   - Decision needed: Session management approach

2. **JWT Verification in FastAPI**
   - Research: python-jose vs PyJWT for JWT validation
   - Research: Middleware vs dependency injection for auth
   - Research: Extracting user_id from JWT claims
   - Decision needed: JWT library selection
   - Decision needed: Token validation approach

3. **Neon PostgreSQL Connection Patterns**
   - Research: Connection pooling with Neon Serverless
   - Research: SQLModel session management with async/await
   - Research: SSL/TLS configuration (sslmode=require, channel_binding=require)
   - Decision needed: Async vs sync database operations
   - Decision needed: Connection pool configuration

4. **User Ownership Enforcement Patterns**
   - Research: Query filtering at ORM level vs application level
   - Research: Preventing SQL injection in user_id validation
   - Research: Error handling for authorization failures (401 vs 403)
   - Decision needed: Ownership enforcement strategy

5. **CORS Configuration**
   - Research: FastAPI CORS middleware configuration
   - Research: Allowed origins for development vs production
   - Decision needed: CORS policy for frontend-backend communication

**Output**: `research.md` with decisions, rationale, and alternatives for each research task

---

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete with all decisions finalized

### 1.1 Data Model Design

**Objective**: Define database schema and SQLModel entities

**Entities to Design**:

1. **User Entity**
   - Fields: id (UUID/int), email (unique), created_at, updated_at
   - Relationships: One-to-many with Task
   - Validation: Email format validation
   - Indexes: Unique index on email

2. **Task Entity**
   - Fields: id (UUID/int), user_id (foreign key), title (required, max 500 chars), description (optional, max 5000 chars), is_completed (boolean, default false), created_at, updated_at
   - Relationships: Many-to-one with User
   - Validation: Title required and non-empty, character limits
   - Indexes: Index on user_id for query performance, composite index on (user_id, created_at) for sorting

**Output**: `data-model.md` with complete entity definitions, relationships, and validation rules

### 1.2 API Contract Design

**Objective**: Define REST API endpoints with request/response schemas

**Endpoints to Design** (all under `/api/` prefix):

1. **GET /api/{user_id}/tasks**
   - Description: List all tasks for authenticated user
   - Path params: user_id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Response 200: Array of task objects
   - Response 401: Unauthorized (missing/invalid token)
   - Response 403: Forbidden (user_id mismatch)

2. **POST /api/{user_id}/tasks**
   - Description: Create new task for authenticated user
   - Path params: user_id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Request body: { title: string, description?: string }
   - Response 201: Created task object
   - Response 400: Bad request (validation error)
   - Response 401: Unauthorized
   - Response 403: Forbidden

3. **GET /api/{user_id}/tasks/{id}**
   - Description: Get specific task by ID
   - Path params: user_id (string), id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Response 200: Task object
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Task not found

4. **PUT /api/{user_id}/tasks/{id}**
   - Description: Update task (title and/or description)
   - Path params: user_id (string), id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Request body: { title?: string, description?: string }
   - Response 200: Updated task object
   - Response 400: Bad request
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Task not found

5. **DELETE /api/{user_id}/tasks/{id}**
   - Description: Delete task permanently
   - Path params: user_id (string), id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Response 204: No content (success)
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Task not found

6. **PATCH /api/{user_id}/tasks/{id}/complete**
   - Description: Toggle task completion status
   - Path params: user_id (string), id (string)
   - Headers: Authorization: Bearer {jwt_token}
   - Request body: { is_completed: boolean }
   - Response 200: Updated task object
   - Response 401: Unauthorized
   - Response 403: Forbidden
   - Response 404: Task not found

**Output**: `contracts/api-spec.yaml` (OpenAPI 3.0 specification with all endpoints, schemas, and error responses)

### 1.3 Quickstart Guide

**Objective**: Document setup and validation steps for developers

**Sections to Include**:
1. Prerequisites (Python 3.11+, Node.js 20+, Neon PostgreSQL account)
2. Environment setup (DATABASE_URL, BETTER_AUTH_SECRET)
3. Backend setup (install dependencies, run migrations, start server on port 8001)
4. Frontend setup (install dependencies, configure Better Auth, start dev server)
5. Validation steps (test authentication, create task, verify user isolation)
6. Common issues and troubleshooting

**Output**: `quickstart.md` with step-by-step setup instructions

### 1.4 Agent Context Update

**Objective**: Update Claude Code context with technology decisions

**Script to Run**: `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Context to Add**:
- FastAPI on port 8001
- SQLModel with Neon PostgreSQL
- Better Auth with JWT
- Next.js 16+ App Router
- User ownership enforcement pattern

**Output**: Updated agent-specific context file with new technology stack

---

## Phase 2: Constitution Re-Check

**Objective**: Verify all design decisions comply with constitution after detailed design

### Re-validation Checklist

- [ ] Data model uses SQLModel (not SQLAlchemy or other ORM)
- [ ] API endpoints all under /api/ prefix
- [ ] Backend configured for port 8001 only
- [ ] JWT validation implemented in middleware
- [ ] User ownership checks in all task queries
- [ ] Environment variables used for DATABASE_URL and BETTER_AUTH_SECRET
- [ ] No hardcoded credentials in any design artifacts
- [ ] Frontend uses Next.js App Router (not Pages Router)
- [ ] Better Auth configured for passwordless authentication

**Expected Result**: All checklist items pass, no constitution violations introduced during design phase

---

## Implementation Phases (Post-Planning)

**Note**: The following phases are for reference only. Actual implementation will be driven by `/sp.tasks` command output.

### Phase 3: Foundation (Backend Core)

**Objective**: Establish backend infrastructure and database connectivity

**Key Deliverables**:
- FastAPI application initialized on port 8001
- Database connection to Neon PostgreSQL via DATABASE_URL
- SQLModel models for User and Task
- Database migrations (if using Alembic)
- Health check endpoint

### Phase 4: Authentication & Authorization

**Objective**: Implement JWT verification and user ownership enforcement

**Key Deliverables**:
- JWT verification middleware
- get_current_user dependency injection
- User ownership validation in all endpoints
- 401/403 error handling

### Phase 5: Task CRUD API

**Objective**: Implement all 6 task management endpoints

**Key Deliverables**:
- GET /api/{user_id}/tasks (list)
- POST /api/{user_id}/tasks (create)
- GET /api/{user_id}/tasks/{id} (read)
- PUT /api/{user_id}/tasks/{id} (update)
- DELETE /api/{user_id}/tasks/{id} (delete)
- PATCH /api/{user_id}/tasks/{id}/complete (toggle completion)

### Phase 6: Frontend Foundation

**Objective**: Set up Next.js application with Better Auth

**Key Deliverables**:
- Next.js 16+ project with App Router
- Better Auth configuration
- Authentication flow (login, callback, logout)
- Protected route middleware
- API client with JWT attachment

### Phase 7: Task UI

**Objective**: Build responsive task management interface

**Key Deliverables**:
- Task list component
- Task creation form
- Task edit/delete functionality
- Task completion toggle
- Loading and error states
- Empty state handling

### Phase 8: Security Validation & Testing

**Objective**: Verify security requirements and user isolation

**Key Deliverables**:
- Test unauthorized access (401 responses)
- Test cross-user access attempts (403 responses)
- Test JWT expiration handling
- Test user ownership enforcement
- Integration tests for all user stories

---

## Risk Analysis

### High Priority Risks

1. **Better Auth Integration Complexity**
   - Risk: Better Auth documentation may be incomplete for Next.js 16+ App Router
   - Mitigation: Research phase will validate integration patterns; fallback to manual JWT handling if needed
   - Impact: Could delay frontend authentication by 1-2 days

2. **Neon PostgreSQL Connection Pooling**
   - Risk: Serverless PostgreSQL may have connection limits or cold start issues
   - Mitigation: Configure connection pooling properly; test under load during validation
   - Impact: Could affect concurrent user support (SC-004)

3. **User Ownership Enforcement Gaps**
   - Risk: Missing ownership check in any endpoint creates security vulnerability
   - Mitigation: Systematic review of all endpoints; integration tests for cross-user access
   - Impact: Critical security issue if not caught

### Medium Priority Risks

4. **JWT Token Storage Security**
   - Risk: localStorage vulnerable to XSS; httpOnly cookies require CORS configuration
   - Mitigation: Research phase will determine best practice; implement CSP headers
   - Impact: Could require frontend architecture changes

5. **CORS Configuration**
   - Risk: Incorrect CORS settings block frontend-backend communication
   - Mitigation: Document CORS configuration in quickstart; test in development environment
   - Impact: Could block frontend development until resolved

---

## Success Criteria Mapping

| Success Criterion | Implementation Phase | Validation Method |
|-------------------|---------------------|-------------------|
| SC-001: Auth flow <30s | Phase 6 (Frontend Auth) | Manual testing with timer |
| SC-002: Task create <2s | Phase 5 (Task API) + Phase 7 (Task UI) | Performance testing |
| SC-003: 100% ownership enforcement | Phase 4 (Auth) + Phase 5 (Task API) | Integration tests for cross-user access |
| SC-004: 100 concurrent users | Phase 3 (Backend Core) | Load testing with 100 simulated users |
| SC-005: Data persistence | Phase 3 (Backend Core) | Restart backend, verify data intact |
| SC-006: 95% operation success | Phase 5 (Task API) | Monitor error rates in testing |
| SC-007: Cross-device access | Phase 6 (Frontend) + Phase 7 (Task UI) | Test on desktop and mobile browsers |
| SC-008: <1s visual feedback | Phase 7 (Task UI) | Frontend performance testing |
| SC-009: 24h token validity | Phase 4 (Auth) | Configure JWT expiration, test token refresh |
| SC-010: 100% error messages | Phase 5 (Task API) + Phase 7 (Task UI) | Test all error scenarios |

---

## Next Steps

1. **Execute Phase 0**: Create `research.md` by researching Better Auth, JWT validation, Neon PostgreSQL patterns, and user ownership enforcement
2. **Execute Phase 1**: Create `data-model.md`, `contracts/api-spec.yaml`, and `quickstart.md` based on research decisions
3. **Run Agent Context Update**: Execute `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
4. **Re-check Constitution**: Verify all design artifacts comply with constitution requirements
5. **Generate Tasks**: Run `/sp.tasks` to create detailed task breakdown for implementation

**Current Status**: Plan complete, ready for Phase 0 research
