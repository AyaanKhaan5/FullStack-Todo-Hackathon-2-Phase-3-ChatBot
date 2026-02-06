---
id: 001
title: Create Project Constitution v1.0.0
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: DELL LATITUDE
command: /sp.constitution
labels: ["constitution", "governance", "non-negotiable-rules", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
sp.constitute  Project Name: Hackathon Todo – Phase II (Full-Stack)  Non-Negotiable Rules: 1. Backend MUST be implemented in Python using FastAPI. 2. Backend server MUST run on port 8001 only. 3. Database MUST be Neon Serverless PostgreSQL. 4. Database connection MUST use the provided Neon connection string ONLY. 5. ORM MUST be SQLModel. 6. Authentication MUST be passwordless and JWT-based using Better Auth. 7. Frontend MUST be Next.js 16+ using App Router. 8. REST API MUST be secured using JWT Bearer tokens. 9. All API routes MUST enforce user ownership on every operation. 10. The application MUST be structured as a monorepo compatible with Spec-Kit Plus. 11. Specs located in /specs are the source of truth. 12. Claude Code MUST read relevant specs before modifying any code. 13. No hardcoded credentials are allowed outside environment variables. 14. No alternative databases, ORMs, auth systems, or ports are allowed.  Failure to follow any rule is considered an invalid implementation.
```

## Response snapshot

Created the project constitution v1.0.0 for Hackathon Todo – Phase II (Full-Stack). The constitution establishes 6 core principles organized into:

1. **Technology Stack (NON-NEGOTIABLE)**: Fixed requirements for FastAPI backend on port 8001, Neon PostgreSQL with SQLModel ORM, and Next.js 16+ frontend
2. **Security & Authentication (NON-NEGOTIABLE)**: Passwordless JWT-based auth using Better Auth, user ownership enforcement on all API routes, environment variable-based credential management
3. **Architecture & Structure (NON-NEGOTIABLE)**: Monorepo structure compatible with Spec-Kit Plus, specification authority from /specs directory
4. **Development Workflow (NON-NEGOTIABLE)**: Specification-first development, small testable changes, precise code references
5. **Configuration Management**: Environment variables for all configuration, fixed port 8001 for backend
6. **Specification Compliance**: Mandatory specs for all features, traceability requirements, ADR documentation for significant decisions

The constitution includes development workflow requirements (pre-implementation, implementation, post-implementation), technology constraints (prohibited alternatives), and governance rules (amendment process, compliance review, complexity justification).

All 14 non-negotiable rules from the user input have been incorporated and organized into a structured, enforceable constitution document.

## Outcome

- ✅ Impact: Established foundational governance document that defines all non-negotiable technical and process requirements for the hackathon project
- 🧪 Tests: No tests required (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md with complete constitution v1.0.0
- 🔁 Next prompts: Feature specification creation (/sp.specify), implementation planning (/sp.plan), or task generation (/sp.tasks)
- 🧠 Reflection: Constitution successfully captures all 14 non-negotiable rules in a structured format with clear rationale, enforcement mechanisms, and governance procedures. Templates reviewed for compatibility.

## Evaluation notes (flywheel)

- Failure modes observed: None - all placeholders filled, no unresolved tokens, proper routing to constitution directory
- Graders run and results (PASS/FAIL): PASS - Constitution complete with all required sections, proper versioning (1.0.0), ratification date set, sync impact report included
- Prompt variant (if applicable): Standard /sp.constitution command execution
- Next experiment (smallest change to try): Monitor template compliance during first feature specification to validate constitution check integration
