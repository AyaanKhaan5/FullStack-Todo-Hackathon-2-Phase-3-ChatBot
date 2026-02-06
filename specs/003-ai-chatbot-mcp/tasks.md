# Tasks: AI-Powered Todo Chatbot with MCP

**Input**: Design documents from `/specs/003-ai-chatbot-mcp/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below follow web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [ ] T001 Install backend Python dependencies (openai, swarm-sdk, python-dateparser, rapidfuzz) in backend/requirements.txt
- [ ] T002 Install frontend npm dependencies (@chatscope/chat-ui-kit-react) in frontend/package.json
- [ ] T003 Add OPENAI_API_KEY and OPENAI_MODEL to backend/.env.example
- [ ] T004 Update backend/src/config.py to load OPENAI_API_KEY from environment

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create Conversation model in backend/src/models/conversation.py with SQLModel schema
- [ ] T006 [P] Create Message model in backend/src/models/message.py with SQLModel schema and MessageRole enum
- [ ] T007 [P] Create Alembic migration script for conversations and messages tables in backend/alembic/versions/003_add_conversations_messages.py
- [ ] T008 Run database migration to create conversations and messages tables
- [ ] T009 [P] Create ChatRequest schema in backend/src/schemas/chat.py
- [ ] T010 [P] Create ChatResponse schema in backend/src/schemas/chat.py
- [ ] T011 [P] Create ConversationSchema in backend/src/schemas/conversation.py
- [ ] T012 [P] Create MessageSchema in backend/src/schemas/message.py
- [ ] T013 Create TaskService class in backend/src/services/task_service.py to extract task CRUD logic from routes
- [ ] T014 Create MCP server class in backend/src/mcp/server.py with create_tool_functions method
- [ ] T015 Create JWT context extraction utility in backend/src/mcp/context.py for passing user_id to MCP tools
- [ ] T016 Create chat route skeleton in backend/src/api/routes/chat.py with JWT authentication dependency
- [ ] T017 Update backend/src/models/__init__.py to export Conversation and Message models
- [ ] T018 Update backend/src/schemas/__init__.py to export chat schemas

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks through natural language in the chatbot

**Independent Test**: User types "add a task to buy groceries tomorrow" → task created and visible in task list UI

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py with natural language date parsing
- [ ] T020 [P] [US1] Create date parsing utility in backend/src/utils/date_parser.py using python-dateparser
- [ ] T021 [US1] Integrate add_task tool into MCP server in backend/src/mcp/server.py
- [ ] T022 [US1] Create AIAgent service in backend/src/services/ai_agent.py with OpenAI Agents SDK and Swarm initialization
- [ ] T023 [US1] Create ChatService in backend/src/services/chat_service.py to orchestrate conversation flow
- [ ] T024 [US1] Implement POST /api/chat endpoint in backend/src/api/routes/chat.py with message processing
- [ ] T025 [US1] Add conversation creation logic in ChatService when conversation_id is null
- [ ] T026 [US1] Add message persistence logic in ChatService for user and assistant messages
- [ ] T027 [US1] Add conversation title auto-generation from first message in ChatService
- [ ] T028 [US1] Register chat route in backend/src/main.py
- [ ] T029 [P] [US1] Create chat types in frontend/src/types/chat.ts for Message, Conversation, ChatRequest, ChatResponse
- [ ] T030 [P] [US1] Create chat API client in frontend/src/lib/chat-api.ts with JWT token passing
- [ ] T031 [P] [US1] Create ChatInterface component in frontend/src/components/chat/ChatInterface.tsx using ChatKit
- [ ] T032 [P] [US1] Create MessageList component in frontend/src/components/chat/MessageList.tsx
- [ ] T033 [P] [US1] Create MessageInput component in frontend/src/components/chat/MessageInput.tsx
- [ ] T034 [P] [US1] Create ChatHeader component in frontend/src/components/chat/ChatHeader.tsx
- [ ] T035 [US1] Create chat page in frontend/src/app/(dashboard)/chat/page.tsx
- [ ] T036 [US1] Add chat navigation link to dashboard layout in frontend/src/app/(dashboard)/layout.tsx
- [ ] T037 [US1] Implement error handling for AI service unavailability in ChatService with graceful fallback messages
- [ ] T038 [US1] Add action tracking in ChatResponse to indicate task_created action

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Conversational Task Management (Priority: P2)

**Goal**: Users can manage tasks (list, complete, update, delete) through natural language

**Independent Test**: User asks "what are my tasks?" → sees list, says "complete the first one" → task marked done

### Implementation for User Story 2

- [ ] T039 [P] [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py with filter support
- [ ] T040 [P] [US2] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py
- [ ] T041 [P] [US2] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py
- [ ] T042 [P] [US2] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py
- [ ] T043 [US2] Integrate all task management tools into MCP server in backend/src/mcp/server.py
- [ ] T044 [US2] Create fuzzy task matching utility in backend/src/utils/task_matcher.py using rapidfuzz
- [ ] T045 [US2] Add task matching logic to complete_task, update_task, and delete_task tools
- [ ] T046 [US2] Update AIAgent instructions in backend/src/services/ai_agent.py to handle all task operations
- [ ] T047 [US2] Add disambiguation prompts in ChatService when multiple tasks match
- [ ] T048 [US2] Add action tracking for task_updated, task_completed, task_deleted, tasks_listed in ChatResponse
- [ ] T049 [US2] Update ChatInterface to display task lists in chat messages
- [ ] T050 [US2] Update ChatInterface to show task action confirmations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Conversation Persistence (Priority: P3)

**Goal**: Users can access conversation history and continue previous conversations

**Independent Test**: User creates tasks in conversation, closes chat, reopens → sees history and can continue

### Implementation for User Story 3

- [ ] T051 [US3] Create GET /api/conversations endpoint in backend/src/api/routes/chat.py to list user's conversations
- [ ] T052 [US3] Create GET /api/conversations/{id}/messages endpoint in backend/src/api/routes/chat.py with pagination
- [ ] T053 [US3] Add conversation history loading in ChatService when conversation_id is provided
- [ ] T054 [US3] Update conversation.updated_at timestamp when new message added in ChatService
- [ ] T055 [P] [US3] Create ConversationList component in frontend/src/components/chat/ConversationList.tsx
- [ ] T056 [US3] Update ChatInterface to load conversation history on mount
- [ ] T057 [US3] Add "New Conversation" button in ChatHeader component
- [ ] T058 [US3] Add conversation selection UI in chat page to switch between conversations
- [ ] T059 [US3] Implement message pagination for long conversations in MessageList component
- [ ] T060 [US3] Add conversation title display in ChatHeader

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T061 [P] Add comprehensive error handling for OpenAI API errors in AIAgent service
- [ ] T062 [P] Add rate limit error handling in ChatService with user-friendly messages
- [ ] T063 [P] Add database error handling in ChatService with graceful fallback
- [ ] T064 Add logging for all chat operations in ChatService
- [ ] T065 Add logging for all MCP tool invocations in MCP server
- [ ] T066 Validate chat response time <3 seconds under normal load
- [ ] T067 Validate task creation time <10 seconds from opening chatbot
- [ ] T068 Test multi-user isolation (User A cannot access User B's tasks via chat)
- [ ] T069 Test stateless restart safety (restart backend mid-conversation, verify continuation works)
- [ ] T070 Validate backward compatibility (Phase II REST APIs unchanged and functional)
- [ ] T071 Test AI service unavailability fallback with graceful error messages
- [ ] T072 Validate 100 concurrent chat sessions without performance degradation
- [ ] T073 Add input validation for chat messages (max length 2000 characters)
- [ ] T074 Add input sanitization to prevent injection attacks in chat messages
- [ ] T075 Run quickstart.md validation checklist
- [ ] T076 Update README.md with Phase III setup instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 but independently testable

### Within Each User Story

- Models and schemas before services
- Services before endpoints
- Backend endpoints before frontend components
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models/schemas within a story marked [P] can run in parallel
- Frontend components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models/schemas for User Story 1 together:
Task T019: "Implement add_task MCP tool in backend/src/mcp/tools/add_task.py"
Task T020: "Create date parsing utility in backend/src/utils/date_parser.py"

# Launch all frontend components for User Story 1 together:
Task T029: "Create chat types in frontend/src/types/chat.ts"
Task T030: "Create chat API client in frontend/src/lib/chat-api.ts"
Task T031: "Create ChatInterface component"
Task T032: "Create MessageList component"
Task T033: "Create MessageInput component"
Task T034: "Create ChatHeader component"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T019-T038)
   - Developer B: User Story 2 (T039-T050)
   - Developer C: User Story 3 (T051-T060)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 76

**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 14 tasks
- Phase 3 (User Story 1 - P1): 20 tasks
- Phase 4 (User Story 2 - P2): 12 tasks
- Phase 5 (User Story 3 - P3): 10 tasks
- Phase 6 (Polish): 16 tasks

**By User Story**:
- User Story 1 (Natural Language Task Creation): 20 tasks
- User Story 2 (Conversational Task Management): 12 tasks
- User Story 3 (Conversation Persistence): 10 tasks
- Infrastructure (Setup + Foundational): 18 tasks
- Cross-cutting (Polish): 16 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel within their phase

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (38 tasks) delivers User Story 1 - Natural Language Task Creation

**Independent Tests**:
- US1: Type "add task to buy milk" → task created in UI
- US2: Ask "what are my tasks?" → see list, say "complete first one" → task done
- US3: Create tasks, close chat, reopen → see history

**Critical Path**: Setup → Foundational → User Story 1 (MVP)

**Backward Compatibility**: T070 validates Phase II REST APIs remain unchanged
