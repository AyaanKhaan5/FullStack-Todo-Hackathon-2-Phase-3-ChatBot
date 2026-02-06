# Implementation Plan: AI-Powered Todo Chatbot with MCP

**Branch**: `003-ai-chatbot-mcp` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot-mcp/spec.md`

## Summary

Add AI-powered conversational interface for task management using OpenAI Agents SDK and Model Context Protocol (MCP) architecture. Users can create, view, update, complete, and delete tasks through natural language commands. The chatbot integrates on top of existing Phase II infrastructure without breaking REST APIs or traditional UI. All MCP tools are stateless and database-backed, enforcing the same JWT-based authentication and user ownership rules as Phase II.

**Core Value**: Enable hands-free task management through natural conversation while maintaining full backward compatibility with existing Phase II functionality.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend)
**Primary Dependencies**:
- Backend: FastAPI, SQLModel, OpenAI Agents SDK, MCP Server SDK
- Frontend: Next.js 16+, React, ChatKit (or @chatscope/chat-ui-kit-react)
**Storage**: Neon Serverless PostgreSQL (existing + new tables for conversations/messages)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Web (backend + frontend monorepo)
**Performance Goals**:
- Chat response time <3 seconds (SC-003)
- Support 100 concurrent chat sessions (SC-010)
- Task creation <10 seconds from chat open (SC-001)
**Constraints**:
- Backend must remain stateless (no in-memory session state)
- MCP tools must be stateless (no state between invocations)
- Zero breaking changes to Phase II REST APIs (SC-008)
- User identity from JWT only (never from request body/URL)
**Scale/Scope**:
- Multi-user system with user isolation
- 30-day conversation history retention (SC-006)
- English language only (Phase III)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Technology Stack ✅ PASS
- ✅ Backend: Python + FastAPI (required)
- ✅ Database: Neon PostgreSQL (required)
- ✅ ORM: SQLModel (required)
- ✅ Frontend: Next.js 16+ (required)
- ✅ Backend port: 8001 (required)

### Principle II: Security & Authentication ✅ PASS
- ✅ JWT-based authentication using Better Auth (required)
- ✅ User identity derived from JWT only (never from request body/URL)
- ✅ User ownership enforcement on all operations
- ✅ Environment variables for secrets (OPENAI_API_KEY, BETTER_AUTH_SECRET)

### Principle III: Architecture & Structure ✅ PASS
- ✅ Monorepo structure maintained (backend/ + frontend/)
- ✅ Spec-driven development (this plan follows spec.md)
- ✅ Spec-Kit Plus conventions followed

### Principle IV: Development Workflow ✅ PASS
- ✅ Specification-first approach (spec.md created before plan)
- ✅ Small, testable changes planned
- ✅ Traceability to spec requirements (FR-010 through FR-037)

### Principle V: Configuration Management ✅ PASS
- ✅ Environment variables for all configuration
- ✅ Backend port 8001 (non-configurable)
- ✅ Frontend port 3000 (default)

### Principle VI: Specification Compliance ✅ PASS
- ✅ Feature specification exists (spec.md)
- ✅ User stories, requirements, success criteria defined
- ✅ Implementation plan references spec requirements

### Principle VII: AI & MCP Integration ✅ PASS
- ✅ OpenAI Agents SDK for AI functionality (required)
- ✅ MCP architecture for AI-system interaction (required)
- ✅ MCP tools are stateless and DB-backed (required)
- ✅ User identity from JWT in MCP tools (required)
- ✅ AI interacts only through MCP tools (required)
- ✅ Backward compatibility with Phase II (required)
- ✅ ChatKit for chatbot UI (required)

**Overall Assessment**: ✅ ALL GATES PASS - Ready for Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot-mcp/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   ├── chat-api.yaml    # OpenAPI spec for chat endpoint
│   └── mcp-tools.yaml   # MCP tool definitions
├── checklists/
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py           # Existing - Task model
│   │   ├── user.py           # Existing - User model
│   │   ├── conversation.py   # NEW - Conversation model
│   │   └── message.py        # NEW - Message model
│   ├── schemas/
│   │   ├── task.py           # Existing - Task schemas
│   │   ├── chat.py           # NEW - Chat request/response schemas
│   │   ├── conversation.py   # NEW - Conversation schemas
│   │   └── message.py        # NEW - Message schemas
│   ├── api/
│   │   ├── routes/
│   │   │   ├── tasks.py      # Existing - Task CRUD endpoints
│   │   │   ├── auth.py       # Existing - Auth endpoints
│   │   │   └── chat.py       # NEW - Chat endpoint
│   │   └── dependencies.py   # Existing - JWT dependency
│   ├── services/
│   │   ├── task_service.py   # NEW - Task business logic (extracted from routes)
│   │   ├── chat_service.py   # NEW - Chat orchestration
│   │   └── ai_agent.py       # NEW - OpenAI Agents SDK integration
│   ├── mcp/
│   │   ├── server.py         # NEW - MCP server setup
│   │   ├── tools/
│   │   │   ├── add_task.py   # NEW - MCP tool for task creation
│   │   │   ├── list_tasks.py # NEW - MCP tool for task listing
│   │   │   ├── complete_task.py # NEW - MCP tool for task completion
│   │   │   ├── update_task.py   # NEW - MCP tool for task update
│   │   │   └── delete_task.py   # NEW - MCP tool for task deletion
│   │   └── context.py        # NEW - JWT context extraction for MCP
│   ├── middleware/
│   │   └── auth.py           # Existing - JWT middleware
│   ├── utils/
│   │   └── jwt.py            # Existing - JWT utilities
│   ├── database.py           # Existing - Database connection
│   ├── config.py             # Existing - Configuration (add OPENAI_API_KEY)
│   └── main.py               # Existing - FastAPI app (add chat route)
└── tests/
    ├── test_chat_api.py      # NEW - Chat endpoint tests
    ├── test_mcp_tools.py     # NEW - MCP tool tests
    └── test_ai_agent.py      # NEW - AI agent tests

frontend/
├── src/
│   ├── app/
│   │   ├── (dashboard)/
│   │   │   ├── page.tsx      # Existing - Task list UI
│   │   │   └── chat/
│   │   │       └── page.tsx  # NEW - Chat interface page
│   │   └── layout.tsx        # Existing - Root layout
│   ├── components/
│   │   ├── tasks/
│   │   │   └── TaskList.tsx  # Existing - Task list component
│   │   └── chat/
│   │       ├── ChatInterface.tsx  # NEW - Main chat component
│   │       ├── MessageList.tsx    # NEW - Message display
│   │       ├── MessageInput.tsx   # NEW - Message input
│   │       └── ChatHeader.tsx     # NEW - Chat header
│   ├── lib/
│   │   ├── api.ts            # Existing - API client
│   │   ├── auth.ts           # Existing - Auth utilities
│   │   └── chat-api.ts       # NEW - Chat API client
│   └── types/
│       ├── task.ts           # Existing - Task types
│       └── chat.ts           # NEW - Chat/message types
└── tests/
    └── chat/
        ├── ChatInterface.test.tsx  # NEW - Chat component tests
        └── chat-api.test.ts        # NEW - Chat API tests
```

**Structure Decision**: Web application structure (Option 2) with backend and frontend directories. This maintains the existing Phase II monorepo structure while adding new AI/MCP components. Backend adds new models (Conversation, Message), MCP server with 5 stateless tools, AI agent service, and chat endpoint. Frontend adds chat UI components using ChatKit. All new code integrates without modifying existing Phase II files.

## Complexity Tracking

> **No constitutional violations - this section intentionally left empty**

All complexity is justified by constitutional requirements:
- OpenAI Agents SDK: Required by Principle VII
- MCP architecture: Required by Principle VII
- Stateless MCP tools: Required by Principle VII
- Conversation/Message models: Required by FR-029 through FR-033
- ChatKit UI: Required by Principle VII

---

## Phase 0: Research & Technology Validation

### Research Objectives

1. **OpenAI Agents SDK Integration**
   - Understand agent initialization and configuration
   - Determine how to connect agents to MCP tools
   - Identify best practices for natural language intent extraction
   - Research error handling and fallback strategies

2. **MCP Server Implementation**
   - Research MCP server setup in Python/FastAPI context
   - Understand how to pass JWT context to stateless MCP tools
   - Determine tool definition format and registration
   - Identify patterns for database access in stateless tools

3. **ChatKit UI Integration**
   - Evaluate ChatKit vs @chatscope/chat-ui-kit-react
   - Understand message rendering and input handling
   - Research JWT token passing in chat requests
   - Identify patterns for real-time message updates

4. **Conversation Persistence**
   - Research efficient conversation history retrieval patterns
   - Determine optimal database schema for messages
   - Identify pagination strategies for long conversations
   - Research conversation context management

5. **Task Matching & Fuzzy Search**
   - Research fuzzy string matching libraries (fuzzywuzzy, rapidfuzz)
   - Determine threshold for task title matching
   - Identify disambiguation strategies for ambiguous matches

### Research Deliverables

See [research.md](./research.md) for detailed findings.

---

## Phase 1: Design & Contracts

### 1.1 Data Model Design

**New Entities** (see [data-model.md](./data-model.md) for complete schema):

1. **Conversation**
   - `id` (UUID, primary key)
   - `user_id` (UUID, foreign key to users.id)
   - `title` (string, optional, auto-generated from first message)
   - `created_at` (timestamp)
   - `updated_at` (timestamp)

2. **Message**
   - `id` (UUID, primary key)
   - `conversation_id` (UUID, foreign key to conversations.id)
   - `role` (enum: 'user' | 'assistant')
   - `content` (text)
   - `created_at` (timestamp)

**Relationships**:
- User → Conversations (one-to-many)
- Conversation → Messages (one-to-many)
- User → Tasks (one-to-many, existing)

**Indexes**:
- `conversations.user_id` (for user's conversation list)
- `messages.conversation_id` (for conversation history)
- `messages.created_at` (for chronological ordering)

### 1.2 API Contracts

**Chat Endpoint** (see [contracts/chat-api.yaml](./contracts/chat-api.yaml)):

```
POST /api/chat
Authorization: Bearer <JWT>
Content-Type: application/json

Request:
{
  "message": "add a task to buy groceries tomorrow",
  "conversation_id": "uuid-or-null"  // null creates new conversation
}

Response:
{
  "conversation_id": "uuid",
  "message": {
    "id": "uuid",
    "role": "assistant",
    "content": "I've created a task 'buy groceries' with due date tomorrow.",
    "created_at": "2026-01-15T10:30:00Z"
  },
  "actions": [
    {
      "type": "task_created",
      "task_id": 123
    }
  ]
}
```

**MCP Tools** (see [contracts/mcp-tools.yaml](./contracts/mcp-tools.yaml)):

1. `add_task(title: str, description: str | None, due_date: str | None) -> Task`
2. `list_tasks(filter: str | None, limit: int = 50) -> List[Task]`
3. `complete_task(task_id: int) -> Task`
4. `update_task(task_id: int, title: str | None, description: str | None, due_date: str | None) -> Task`
5. `delete_task(task_id: int) -> bool`

All tools receive JWT context automatically and enforce user ownership.

### 1.3 Quickstart Guide

See [quickstart.md](./quickstart.md) for:
- Environment setup (OPENAI_API_KEY)
- Database migration steps
- MCP server startup
- Frontend chat UI access
- Testing checklist

---

## Phase 2: Implementation Roadmap

**Note**: Detailed tasks will be generated by `/sp.tasks` command. This section provides high-level implementation phases aligned with user stories.

### Phase 2.1: Foundation (Blocking Prerequisites)

**Purpose**: Core infrastructure that must be complete before any user story

- Database schema migration (Conversation, Message models)
- MCP server setup and tool registration framework
- JWT context extraction for MCP tools
- Chat endpoint skeleton (authentication only)
- Task service extraction (move logic from routes to service layer)

**Checkpoint**: Foundation ready - user story implementation can begin

### Phase 2.2: User Story 1 - Natural Language Task Creation (P1) 🎯 MVP

**Goal**: Users can create tasks through natural language

**Implementation**:
- OpenAI Agents SDK integration
- MCP tool: `add_task` (stateless, DB-backed)
- AI agent intent extraction for task creation
- Chat endpoint: message processing and response
- Conversation/message persistence
- Frontend: Basic chat UI with message input
- Frontend: Display assistant responses

**Independent Test**: User types "add task to buy milk" → task created and visible in task list

### Phase 2.3: User Story 2 - Conversational Task Management (P2)

**Goal**: Users can manage tasks through natural language

**Implementation**:
- MCP tools: `list_tasks`, `complete_task`, `update_task`, `delete_task`
- AI agent intent extraction for all task operations
- Fuzzy task matching for ambiguous references
- Disambiguation prompts for multiple matches
- Frontend: Display task lists in chat
- Frontend: Show task action confirmations

**Independent Test**: User asks "what are my tasks?" → sees list, says "complete the first one" → task marked done

### Phase 2.4: User Story 3 - Conversation Persistence (P3)

**Goal**: Users can access conversation history

**Implementation**:
- Conversation history retrieval endpoint
- Frontend: Load and display conversation history
- Frontend: Conversation list/selection UI
- Frontend: "New conversation" functionality
- Message pagination for long conversations

**Independent Test**: User creates tasks in conversation, closes chat, reopens → sees history

### Phase 2.5: Polish & Integration

**Purpose**: Cross-cutting concerns and validation

- Error handling for AI service unavailability (FR-018)
- Graceful fallback messages
- Performance optimization (response time <3s)
- Multi-user isolation testing
- Stateless restart safety testing
- Backward compatibility validation (Phase II APIs unchanged)
- End-to-end testing across all user stories

---

## Risk Analysis

### High Priority Risks

1. **OpenAI API Rate Limits**
   - **Risk**: Exceeding API quota during high usage
   - **Mitigation**: Implement rate limiting, queue requests, monitor usage
   - **Fallback**: Graceful error messages (FR-018)

2. **MCP Tool Statefulness Violation**
   - **Risk**: Accidentally introducing in-memory state in MCP tools
   - **Mitigation**: Code review checklist, stateless restart tests
   - **Detection**: Test server restart mid-conversation

3. **User Identity Spoofing**
   - **Risk**: MCP tools accepting user_id from request instead of JWT
   - **Mitigation**: Strict JWT context extraction, security review
   - **Detection**: Multi-user isolation tests

4. **Backward Compatibility Break**
   - **Risk**: Modifying Phase II REST APIs or database schema
   - **Mitigation**: No changes to existing endpoints, additive schema changes only
   - **Detection**: Phase II regression tests

### Medium Priority Risks

5. **Task Matching Ambiguity**
   - **Risk**: Fuzzy matching selects wrong task
   - **Mitigation**: Disambiguation prompts, match confidence thresholds
   - **Fallback**: Ask user to clarify

6. **Conversation History Performance**
   - **Risk**: Slow retrieval for users with many messages
   - **Mitigation**: Pagination, database indexes, limit history to 30 days
   - **Detection**: Load testing with large conversation histories

---

## Dependencies & Prerequisites

### External Dependencies

1. **OpenAI API Access**
   - Requires: Valid API key with sufficient quota
   - Setup: Add OPENAI_API_KEY to backend/.env
   - Validation: Test API connection during startup

2. **ChatKit or @chatscope/chat-ui-kit-react**
   - Requires: npm package installation
   - Setup: `npm install @chatscope/chat-ui-kit-react`
   - Validation: Component renders in development

### Internal Dependencies

3. **Phase II Infrastructure** (Already Implemented)
   - Task model and CRUD operations (backend/src/models/task.py)
   - JWT authentication middleware (backend/src/middleware/auth.py)
   - Better Auth integration (frontend)
   - Database connection (backend/src/database.py)

4. **Database Migration Capability**
   - Requires: Alembic or SQLModel migration support
   - Setup: Migration scripts for Conversation and Message tables
   - Validation: Migrations run successfully on Neon PostgreSQL

---

## Success Validation

### Acceptance Criteria Mapping

**User Story 1 (P1)**:
- ✅ SC-001: Task creation <10 seconds
- ✅ SC-002: 90% correct interpretation
- ✅ SC-003: Response time <3 seconds
- ✅ SC-004: Tasks visible in UI immediately

**User Story 2 (P2)**:
- ✅ SC-005: UI tasks accessible via chat
- ✅ SC-007: All CRUD operations via NL

**User Story 3 (P3)**:
- ✅ SC-006: 30-day history retention

**Cross-Cutting**:
- ✅ SC-008: Zero breaking changes
- ✅ SC-009: Graceful AI fallback
- ✅ SC-010: 100 concurrent sessions

### Testing Strategy

1. **Unit Tests**
   - MCP tool functions (stateless validation)
   - AI agent intent extraction
   - Task matching logic
   - JWT context extraction

2. **Integration Tests**
   - Chat endpoint with real database
   - MCP tools with database operations
   - Conversation persistence
   - Multi-user isolation

3. **Contract Tests**
   - Chat API request/response format
   - MCP tool signatures
   - Phase II REST API unchanged

4. **End-to-End Tests**
   - Complete user journeys for each story
   - Cross-UI validation (chat → UI, UI → chat)
   - Stateless restart safety

---

## Next Steps

1. **Complete Phase 0**: Generate research.md with technology findings
2. **Complete Phase 1**: Generate data-model.md, contracts/, quickstart.md
3. **Run `/sp.tasks`**: Generate detailed task breakdown
4. **Begin Implementation**: Start with Phase 2.1 (Foundation)

**Ready for**: Phase 0 research and Phase 1 design artifacts generation.
