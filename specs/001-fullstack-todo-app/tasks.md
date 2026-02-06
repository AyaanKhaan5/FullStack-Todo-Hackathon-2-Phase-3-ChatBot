---

description: "Task list for Full-Stack Todo Web Application implementation"
---

# Tasks: Full-Stack Todo Web Application

**Input**: Design documents from `/specs/001-fullstack-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/api-spec.yaml, research.md, quickstart.md

**Tests**: Tests are OPTIONAL - not explicitly requested in feature specification. Focus on implementation and manual validation per acceptance scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Monorepo structure**: `backend/` and `frontend/` at repository root
- Backend paths: `backend/src/`, `backend/tests/`
- Frontend paths: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create monorepo directory structure (backend/, frontend/, specs/, .gitignore)
- [x] T002 [P] Initialize backend Python project with requirements.txt in backend/
- [x] T003 [P] Initialize frontend Next.js 16+ project with TypeScript in frontend/
- [x] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS, PORT
- [x] T005 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL
- [x] T006 [P] Configure Tailwind CSS in frontend/tailwind.config.ts
- [x] T007 [P] Create backend/src/__init__.py and frontend/src/ directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create backend/src/config.py to load environment variables (DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS, PORT)
- [ ] T009 Create backend/src/database.py with SQLModel engine and get_session dependency for Neon PostgreSQL
- [ ] T010 [P] Create backend/src/models/__init__.py
- [ ] T011 [P] Create backend/src/models/user.py with User SQLModel (id: UUID, email: str, created_at, updated_at)
- [ ] T012 [P] Create backend/src/models/task.py with Task SQLModel (id: int, user_id: UUID FK, title: str, description: Optional[str], is_completed: bool, created_at, updated_at)
- [ ] T013 Initialize Alembic in backend/ directory for database migrations
- [ ] T014 Create initial Alembic migration for users and tasks tables
- [ ] T015 Run Alembic migration to create database schema in Neon PostgreSQL
- [ ] T016 Create backend/src/middleware/__init__.py
- [ ] T017 Create backend/src/middleware/auth.py with JWT verification using python-jose
- [ ] T018 Create backend/src/api/dependencies.py with get_current_user dependency (extracts user_id from JWT)
- [ ] T019 Create backend/src/schemas/__init__.py
- [ ] T020 [P] Create backend/src/schemas/task.py with Pydantic schemas (TaskCreate, TaskUpdate, TaskComplete, TaskResponse)
- [ ] T021 [P] Create backend/src/schemas/user.py with Pydantic schemas (UserResponse)
- [ ] T022 Create backend/src/main.py with FastAPI app initialization on port 8001
- [ ] T023 Add CORS middleware to backend/src/main.py with ALLOWED_ORIGINS from environment
- [ ] T024 Create backend/src/api/__init__.py
- [ ] T025 Create backend/src/api/routes/__init__.py
- [ ] T026 Create frontend/src/lib/auth.ts with Better Auth configuration (passwordless email provider)
- [ ] T027 Create frontend/src/lib/api.ts with API client wrapper (includes credentials for httpOnly cookies)
- [ ] T028 Create frontend/src/lib/types.ts with TypeScript interfaces (Task, User)
- [ ] T029 Create frontend/src/app/layout.tsx with root layout and Better Auth provider
- [ ] T030 Create frontend/src/app/globals.css with Tailwind CSS imports
- [ ] T031 Create frontend/src/components/AuthProvider.tsx with Better Auth context

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authenticated Task Viewing (Priority: P1) 🎯 MVP

**Goal**: Users can authenticate and view their personal task list with complete data isolation

**Independent Test**: Authenticate a user, verify they see only their own tasks (or empty list for new users). Create tasks as User A, authenticate as User B, verify User B sees empty list.

### Implementation for User Story 1

- [ ] T032 [P] [US1] Create backend/src/api/routes/tasks.py with router initialization
- [ ] T033 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py with user_id validation and ownership filtering
- [ ] T034 [US1] Register tasks router in backend/src/main.py
- [ ] T035 [US1] Create frontend/src/app/page.tsx with landing/login page using Better Auth
- [ ] T036 [US1] Create frontend/src/app/auth/callback/page.tsx for Better Auth callback handling
- [ ] T037 [US1] Create frontend/src/app/tasks/layout.tsx with protected route middleware (redirects unauthenticated users)
- [ ] T038 [US1] Create frontend/src/app/tasks/page.tsx with task list page
- [ ] T039 [P] [US1] Create frontend/src/components/TaskList.tsx component to display tasks
- [ ] T040 [P] [US1] Create frontend/src/components/TaskItem.tsx component for individual task display
- [ ] T041 [US1] Implement API call in frontend/src/app/tasks/page.tsx to fetch tasks from GET /api/{user_id}/tasks
- [ ] T042 [US1] Add loading state handling in frontend/src/components/TaskList.tsx
- [ ] T043 [US1] Add empty state handling (welcome message) in frontend/src/components/TaskList.tsx
- [ ] T044 [US1] Add error state handling (401, 403, network errors) in frontend/src/components/TaskList.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can authenticate and view their task list.

**Validation Steps for US1**:
1. Start backend on port 8001, start frontend on port 3000
2. Visit http://localhost:3000, complete passwordless authentication
3. Verify redirect to /tasks page with empty list (new user) or existing tasks
4. Create tasks manually in database for user, refresh page, verify tasks appear
5. Authenticate as different user, verify they see different tasks (data isolation)

---

## Phase 4: User Story 2 - Task Creation (Priority: P2)

**Goal**: Authenticated users can create new tasks that appear immediately in their list

**Independent Test**: Authenticate a user, create a new task, verify it appears in their list and is not visible to other users. Refresh page, verify task persists.

### Implementation for User Story 2

- [ ] T045 [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py with user_id validation and automatic user association
- [ ] T046 [US2] Add title validation (non-empty, max 500 chars) in POST endpoint
- [ ] T047 [US2] Add description validation (optional, max 5000 chars) in POST endpoint
- [ ] T048 [US2] Create frontend/src/components/TaskForm.tsx component with title and description inputs
- [ ] T049 [US2] Add form validation in TaskForm.tsx (title required, character limits)
- [ ] T050 [US2] Implement task creation API call in TaskForm.tsx to POST /api/{user_id}/tasks
- [ ] T051 [US2] Add TaskForm component to frontend/src/app/tasks/page.tsx
- [ ] T052 [US2] Implement optimistic UI update in TaskList.tsx (add task immediately, rollback on error)
- [ ] T053 [US2] Add success feedback (toast/message) in TaskForm.tsx after task creation
- [ ] T054 [US2] Add error handling (400 validation errors, 401, 403) in TaskForm.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can view and create tasks.

**Validation Steps for US2**:
1. Authenticate as user, navigate to /tasks page
2. Enter task title "Test task", optional description "Test description"
3. Click create/submit, verify task appears in list immediately
4. Refresh page, verify task persists
5. Authenticate as different user, verify they don't see the created task
6. Test validation: try creating task with empty title, verify error message

---

## Phase 5: User Story 3 - Task Editing and Deletion (Priority: P3)

**Goal**: Authenticated users can edit and delete their own tasks with ownership enforcement

**Independent Test**: Authenticate a user, edit one of their tasks, delete another task, verify changes persist and other users' tasks remain unaffected.

### Implementation for User Story 3

- [ ] T055 [P] [US3] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py with ownership check
- [ ] T056 [P] [US3] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py with ownership check and validation
- [ ] T057 [P] [US3] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py with ownership check
- [ ] T058 [US3] Add edit mode state to TaskItem.tsx component
- [ ] T059 [US3] Add inline edit form in TaskItem.tsx (title and description inputs)
- [ ] T060 [US3] Implement task update API call in TaskItem.tsx to PUT /api/{user_id}/tasks/{id}
- [ ] T061 [US3] Add delete button to TaskItem.tsx
- [ ] T062 [US3] Add delete confirmation dialog in TaskItem.tsx
- [ ] T063 [US3] Implement task delete API call in TaskItem.tsx to DELETE /api/{user_id}/tasks/{id}
- [ ] T064 [US3] Update TaskList.tsx to remove deleted task from UI
- [ ] T065 [US3] Add error handling for 403 Forbidden (cross-user access attempt) in TaskItem.tsx
- [ ] T066 [US3] Add error handling for 404 Not Found in TaskItem.tsx

**Checkpoint**: All CRUD operations (Create, Read, Update, Delete) should now be functional independently.

**Validation Steps for US3**:
1. Authenticate as user with existing tasks
2. Click edit on a task, change title to "Updated task", save
3. Verify updated title displays immediately and persists after refresh
4. Click delete on a task, confirm deletion
5. Verify task disappears immediately and doesn't reappear after refresh
6. Test cross-user protection: manually call API with another user's task ID, verify 403 error

---

## Phase 6: User Story 4 - Task Completion Status (Priority: P4)

**Goal**: Users can mark tasks as complete/incomplete with visual indicators

**Independent Test**: Authenticate a user, mark a task as complete, verify visual indicator changes and status persists across page refreshes.

### Implementation for User Story 4

- [ ] T067 [US4] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py with ownership check
- [ ] T068 [US4] Add is_completed toggle validation in PATCH endpoint (boolean required)
- [ ] T069 [US4] Add completion checkbox/toggle to TaskItem.tsx component
- [ ] T070 [US4] Add visual styling for completed tasks in TaskItem.tsx (strikethrough, checkmark, opacity)
- [ ] T071 [US4] Implement completion toggle API call in TaskItem.tsx to PATCH /api/{user_id}/tasks/{id}/complete
- [ ] T072 [US4] Add optimistic UI update for completion status in TaskItem.tsx
- [ ] T073 [US4] Add error handling for completion toggle failures in TaskItem.tsx
- [ ] T074 [US4] Update TaskList.tsx to visually distinguish completed vs incomplete tasks

**Checkpoint**: All user stories should now be independently functional. Full CRUD + completion tracking implemented.

**Validation Steps for US4**:
1. Authenticate as user with existing tasks
2. Click checkbox/toggle on an incomplete task
3. Verify task displays completion indicator (strikethrough, checkmark)
4. Refresh page, verify task remains marked as complete
5. Click checkbox/toggle again to mark incomplete
6. Verify task returns to active visual state

---

## Phase 7: Security Validation & Testing

**Purpose**: Verify security requirements and user isolation

- [ ] T075 Test unauthorized access: Call API endpoints without JWT token, verify 401 Unauthorized responses
- [ ] T076 Test expired token handling: Use expired JWT token, verify 401 Unauthorized and frontend redirects to login
- [ ] T077 Test cross-user access prevention: User A attempts to access User B's tasks via API, verify 403 Forbidden
- [ ] T078 Test user_id mismatch: JWT contains user_id X, URL contains user_id Y, verify 403 Forbidden
- [ ] T079 Test malformed JWT: Send invalid JWT token, verify 401 Unauthorized
- [ ] T080 Test SQL injection prevention: Attempt SQL injection in task title/description, verify parameterized queries prevent injection
- [ ] T081 Test XSS prevention: Create task with XSS payload in title, verify frontend sanitizes/escapes content
- [ ] T082 Test CORS configuration: Verify frontend can make requests to backend, unauthorized origins are blocked
- [ ] T083 Verify all API endpoints enforce user ownership (user_id validation in every endpoint)
- [ ] T084 Verify no hardcoded credentials in source code (all secrets from environment variables)

---

## Phase 8: Final Validation & Constitution Compliance

**Purpose**: Verify all constitution requirements and acceptance scenarios

- [ ] T085 Verify backend runs ONLY on port 8001 (check backend/src/config.py and backend/src/main.py)
- [ ] T086 Verify Neon PostgreSQL is used exclusively (check DATABASE_URL in backend/.env, no SQLite/local DB)
- [ ] T087 Verify SQLModel ORM is used (check backend/src/models/, no raw SQL or other ORMs)
- [ ] T088 Verify Better Auth passwordless authentication works end-to-end (test magic link flow)
- [ ] T089 Verify JWT tokens are issued and validated correctly (check Authorization header in requests)
- [ ] T090 Verify Next.js 16+ App Router is used (check frontend/src/app/ structure, no pages/ directory)
- [ ] T091 Verify FastAPI is used for backend (check backend/src/main.py)
- [ ] T092 Verify monorepo structure with backend/ and frontend/ directories
- [ ] T093 Verify Spec-Kit Plus compliance (check /specs directory structure)
- [ ] T094 Verify all environment variables are loaded from .env files (no hardcoded secrets)
- [ ] T095 Test User Story 1 acceptance scenarios (4 scenarios from spec.md)
- [ ] T096 Test User Story 2 acceptance scenarios (4 scenarios from spec.md)
- [ ] T097 Test User Story 3 acceptance scenarios (4 scenarios from spec.md)
- [ ] T098 Test User Story 4 acceptance scenarios (4 scenarios from spec.md)
- [ ] T099 Verify success criteria SC-001: Authentication flow completes in under 30 seconds
- [ ] T100 Verify success criteria SC-002: Task creation appears in list within 2 seconds
- [ ] T101 Verify success criteria SC-003: 100% user ownership enforcement (no cross-user data leakage)
- [ ] T102 Verify success criteria SC-004: System handles 100 concurrent users (load testing)
- [ ] T103 Verify success criteria SC-005: Task data persists across application restarts
- [ ] T104 Verify success criteria SC-008: User actions have visual feedback within 1 second

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T105 [P] Add loading spinners/skeletons to all async operations in frontend
- [ ] T106 [P] Add user-friendly error messages for all error scenarios (network, validation, auth)
- [ ] T107 [P] Add responsive design testing (desktop, tablet, mobile) for all frontend components
- [ ] T108 [P] Add accessibility improvements (ARIA labels, keyboard navigation) to frontend components
- [ ] T109 [P] Add API response time logging in backend/src/main.py
- [ ] T110 [P] Add database query performance monitoring in backend/src/database.py
- [ ] T111 [P] Create backend/README.md with setup instructions
- [ ] T112 [P] Create frontend/README.md with setup instructions
- [ ] T113 [P] Update root README.md with monorepo overview and quickstart
- [ ] T114 [P] Add health check endpoint GET /health in backend/src/main.py
- [ ] T115 Run quickstart.md validation (follow all setup steps, verify they work)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Security Validation (Phase 7)**: Depends on all user stories being complete
- **Final Validation (Phase 8)**: Depends on all user stories being complete
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Requires tasks to exist (from US2) but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Requires tasks to exist (from US2) but independently testable

### Within Each User Story

- Backend endpoints before frontend components that call them
- Models and schemas before endpoints that use them
- Core implementation before error handling and edge cases
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tasks within a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch parallel tasks for User Story 1:
Task T032: "Create backend/src/api/routes/tasks.py with router initialization"
Task T039: "Create frontend/src/components/TaskList.tsx component"
Task T040: "Create frontend/src/components/TaskItem.tsx component"

# These can run in parallel because they touch different files
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T032-T044)
   - Developer B: User Story 2 (T045-T054)
   - Developer C: User Story 3 (T055-T066)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Tests are OPTIONAL - focus on manual validation per acceptance scenarios
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 115
- Phase 1 (Setup): 7 tasks
- Phase 2 (Foundational): 24 tasks (BLOCKING)
- Phase 3 (US1 - MVP): 13 tasks
- Phase 4 (US2): 10 tasks
- Phase 5 (US3): 12 tasks
- Phase 6 (US4): 8 tasks
- Phase 7 (Security): 10 tasks
- Phase 8 (Final Validation): 20 tasks
- Phase 9 (Polish): 11 tasks

**Parallel Opportunities**: 35 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phases 1-3 (44 tasks) deliver User Story 1 - authenticated task viewing

**Independent Test Criteria**:
- US1: Authenticate user, verify they see only their tasks
- US2: Create task, verify it appears and persists
- US3: Edit and delete tasks, verify changes persist
- US4: Toggle completion, verify visual indicator and persistence
