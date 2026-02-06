---
id: 002
title: phase-iii-ai-mcp-constitution
stage: constitution
date: 2026-01-15
surface: CLI
model: claude-sonnet-4-5-20250929
feature: N/A
branch: main
user: tanzeel
command: /sp.constitution
labels: [constitution, phase-iii, ai-integration, mcp, openai-agents-sdk]
links:
  spec: N/A
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    action: updated
    lines_changed: 47
tests:
  - N/A
---

## Prompt

```text
sp.constitution

Project: Hackathon II Todo App

Phase II:
- Full-stack Todo web app already implemented
- Next.js App Router frontend
- FastAPI backend + SQLModel
- Neon PostgreSQL
- Better Auth with JWT
- REST APIs for task CRUD

Phase III Goal:
Add AI-powered Todo Chatbot using OpenAI Agents SDK + MCP
without breaking Phase II.

Rules:
- Spec-Kit Plus is source of truth
- Backend must be stateless
- Auth via JWT only (user from token)
- Users only access their own data
- MCP tools are stateless and DB-backed
- AI interacts only through MCP tools

Stack locked. No new auth system.
```

## Response snapshot

Updated project constitution from v1.0.0 to v1.1.0 with Phase III AI/MCP integration requirements.

**Key Changes:**
1. Added Principle VII: AI & MCP Integration with 8 non-negotiable rules
2. Clarified user identity derivation (JWT only, never from request body/URL)
3. Added backward compatibility requirement for Phase II APIs
4. Updated project title to reflect Phase II → Phase III upgrade path

**New Principle VII covers:**
- OpenAI Agents SDK requirement for AI functionality
- MCP architecture for AI-system interaction
- Stateless MCP tools with database persistence
- User identity from JWT tokens only (prevents AI-based security bypasses)
- Same user ownership rules as REST APIs
- No direct database access by AI agents
- Backward compatibility with Phase II
- ChatKit UI requirement for chatbot interface

**Version Bump Rationale:**
MINOR version bump (1.0.0 → 1.1.0) because:
- New principle added (VII. AI & MCP Integration)
- No existing principles removed or redefined
- Backward compatible with Phase II
- Material expansion of governance scope

**Templates Status:**
- ✅ spec-template.md - Compatible, no changes needed
- ✅ plan-template.md - Constitution check will validate Phase III principles
- ✅ tasks-template.md - Task structure supports AI/MCP phases
- ✅ Commands - Will enforce Phase III constitution checks

## Outcome

- ✅ Impact: Constitution updated to govern Phase III AI/MCP integration while preserving Phase II integrity
- 🧪 Tests: N/A (constitution is governance document)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify for Phase III feature specification
- 🧠 Reflection: Successfully added AI/MCP governance without breaking existing Phase II rules. Clear separation of concerns between REST APIs and MCP tools, both enforcing same security model.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
