---
id: 002
title: ai-chatbot-mcp-implementation-plan
stage: plan
date: 2026-01-15
surface: CLI
model: claude-sonnet-4-5-20250929
feature: 003-ai-chatbot-mcp
branch: 003-ai-chatbot-mcp
user: tanzeel
command: /sp.plan
labels: [plan, ai-chatbot, mcp, openai-agents-sdk, phase-iii, architecture, design]
links:
  spec: specs/003-ai-chatbot-mcp/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/003-ai-chatbot-mcp/plan.md
    action: created
    lines_changed: 511
  - path: specs/003-ai-chatbot-mcp/research.md
    action: created
    lines_changed: 350
  - path: specs/003-ai-chatbot-mcp/data-model.md
    action: created
    lines_changed: 450
  - path: specs/003-ai-chatbot-mcp/contracts/mcp-tools.md
    action: created
    lines_changed: 420
  - path: specs/003-ai-chatbot-mcp/contracts/chat-api.yaml
    action: created
    lines_changed: 380
  - path: specs/003-ai-chatbot-mcp/quickstart.md
    action: created
    lines_changed: 450
tests:
  - N/A (planning phase)
---

## Prompt

```text
sp.plan

Create implementation plan for Hackathon II Todo App.

Steps:

1) Phase II validation
- Ensure JWT auth works
- Ensure task ownership enforced

2) Backend
- Add Conversation & Message models
- Add POST /api/chat endpoint
- Load/store chat history

3) MCP
- Setup MCP server
- Implement task tools using existing CRUD logic

4) AI Agent
- Setup OpenAI Agents SDK
- Connect agent to MCP tools
- Define intent → tool mapping

5) Frontend
- Add ChatKit UI
- Send JWT with chat requests
- Show conversation history

6) Testing
- JWT enforcement
- Multi-user isolation
- Stateless restart safety

Reference specs in each step.
```

## Response snapshot

Created comprehensive implementation plan for Phase III AI-Powered Todo Chatbot with MCP integration.

**Planning Artifacts Created**:

1. **plan.md** (511 lines)
   - Technical context and constitution check (all gates pass)
   - Project structure (backend + frontend with new AI/MCP components)
   - Phase 0: Research objectives (OpenAI SDK, MCP, ChatKit, fuzzy matching)
   - Phase 1: Design & contracts (data model, API contracts, quickstart)
   - Phase 2: Implementation roadmap (5 phases aligned with user stories)
   - Risk analysis (6 risks identified with mitigations)
   - Success validation strategy

2. **research.md** (350 lines)
   - OpenAI Agents SDK with Swarm pattern (decision + rationale)
   - Embedded MCP server architecture (stateless, DB-backed)
   - ChatKit UI library selection (@chatscope/chat-ui-kit-react)
   - Conversation persistence strategy (PostgreSQL with indexes)
   - Task matching with rapidfuzz (fuzzy search, 70+ threshold)
   - Error handling patterns (graceful degradation)
   - Security patterns (JWT context extraction)

3. **data-model.md** (450 lines)
   - Complete SQLModel schemas for Conversation and Message entities
   - Entity relationships and indexes
   - Alembic migration script
   - Query patterns with examples
   - User ownership enforcement patterns
   - Performance considerations

4. **contracts/mcp-tools.md** (420 lines)
   - 5 MCP tool specifications (add_task, list_tasks, complete_task, update_task, delete_task)
   - Stateless validation checklist
   - Natural language date parsing
   - Error handling and user-friendly messages
   - Testing strategy for stateless tools

5. **contracts/chat-api.yaml** (380 lines)
   - OpenAPI 3.0 specification for chat endpoint
   - Request/response schemas with examples
   - Conversation listing and message retrieval endpoints
   - JWT authentication requirements
   - Error response formats

6. **quickstart.md** (450 lines)
   - Step-by-step setup guide (10 steps)
   - Environment configuration (OPENAI_API_KEY)
   - Database migration instructions
   - Validation checklist (Phase II compatibility + Phase III functionality)
   - Security validation (JWT enforcement, multi-user isolation)
   - Performance validation (response time, concurrent sessions)
   - Stateless validation (server restart test)
   - Troubleshooting guide
   - Rollback plan

**Constitutional Compliance**:
- ✅ All 7 principles validated and passing
- ✅ Technology stack: Python/FastAPI, Neon PostgreSQL, SQLModel, Next.js
- ✅ Security: JWT-only user identity, user ownership enforcement
- ✅ AI/MCP: OpenAI Agents SDK, stateless MCP tools, backward compatibility
- ✅ No constitutional violations

**Architecture Decisions**:
1. Embedded MCP server in FastAPI (vs separate process)
2. OpenAI Agents SDK with Swarm pattern (vs LangChain)
3. @chatscope/chat-ui-kit-react (vs custom UI)
4. rapidfuzz for task matching (vs semantic search)
5. Stateless tools with user_id closure (vs stateful server)

**Key Design Patterns**:
- MCP tools created per request with JWT-derived user context
- Database session per tool invocation (stateless)
- Conversation history loaded from DB (no in-memory state)
- Fuzzy matching with confirmation for ambiguous tasks
- Graceful degradation for AI service failures

**Implementation Phases**:
- Phase 2.1: Foundation (database, MCP setup, JWT context)
- Phase 2.2: User Story 1 - Natural Language Task Creation (P1 MVP)
- Phase 2.3: User Story 2 - Conversational Task Management (P2)
- Phase 2.4: User Story 3 - Conversation Persistence (P3)
- Phase 2.5: Polish & Integration (error handling, testing)

**Risk Mitigation**:
- OpenAI rate limits: Rate limiting + graceful fallback
- MCP statefulness: Code review + restart tests
- User identity spoofing: Strict JWT extraction + security review
- Backward compatibility: No Phase II changes + regression tests

## Outcome

- ✅ Impact: Complete implementation plan with research, design, and contracts ready for /sp.tasks
- 🧪 Tests: Testing strategy defined (unit, integration, contract, E2E)
- 📁 Files: 6 planning artifacts created (2,561 total lines)
- 🔁 Next prompts: /sp.tasks to generate detailed task breakdown
- 🧠 Reflection: Successfully designed Phase III architecture that integrates cleanly with Phase II without breaking changes. Stateless MCP tools with JWT context ensure security and scalability. All constitutional requirements met. Ready for task generation and implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (all 7 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
