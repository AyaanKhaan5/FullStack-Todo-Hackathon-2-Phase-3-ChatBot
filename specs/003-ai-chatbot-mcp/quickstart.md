# Quickstart Guide: AI-Powered Todo Chatbot with MCP

**Feature**: 003-ai-chatbot-mcp
**Date**: 2026-01-15
**Branch**: `003-ai-chatbot-mcp`

## Overview

This guide walks through setting up and validating the Phase III AI chatbot functionality. Follow these steps to get the chatbot running locally.

---

## Prerequisites

### Phase II Must Be Working

Before starting Phase III, verify Phase II is functional:

```bash
# Backend running on port 8001
curl http://localhost:8001/health
# Should return: {"status": "healthy"}

# Frontend running on port 3000
# Open browser: http://localhost:3000
# Should see task list UI and be able to log in
```

### Required Tools

- Python 3.11+
- Node.js 20+
- PostgreSQL client (for migrations)
- OpenAI API key

---

## Step 1: Environment Configuration

### Backend Environment Variables

Add to `backend/.env`:

```bash
# Existing Phase II variables (DO NOT CHANGE)
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your-secret-here
PORT=8001

# NEW Phase III variables
OPENAI_API_KEY=sk-proj-...  # Your OpenAI API key
OPENAI_MODEL=gpt-4o-mini     # Or gpt-4o for better quality
```

**Get OpenAI API Key**:
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Copy to `OPENAI_API_KEY` in `.env`
4. Ensure sufficient quota/credits

### Frontend Environment Variables

No changes needed to `frontend/.env.local` - existing Better Auth configuration works.

---

## Step 2: Install Dependencies

### Backend Dependencies

```bash
cd backend

# Install new Python packages
pip install openai swarm-sdk python-dateparser rapidfuzz

# Or update requirements.txt and install
pip install -r requirements.txt
```

**New Dependencies**:
- `openai`: OpenAI API client
- `swarm-sdk`: OpenAI Agents SDK (Swarm pattern)
- `python-dateparser`: Natural language date parsing
- `rapidfuzz`: Fuzzy string matching for task names

### Frontend Dependencies

```bash
cd frontend

# Install chat UI library
npm install @chatscope/chat-ui-kit-react

# Install if needed
npm install
```

---

## Step 3: Database Migration

### Run Migration

```bash
cd backend

# Generate migration (if using Alembic auto-generation)
alembic revision --autogenerate -m "Add conversations and messages tables"

# Or use pre-written migration
# Copy migration file to alembic/versions/003_add_conversations_messages.py

# Apply migration
alembic upgrade head

# Verify migration
alembic current
# Should show: 003 (head)
```

### Verify Tables Created

```bash
# Connect to database
psql $DATABASE_URL

# Check tables exist
\dt

# Should see:
# - conversations
# - messages
# - tasks (existing)
# - users (existing)

# Check conversation schema
\d conversations

# Check message schema
\d messages

# Exit
\q
```

---

## Step 4: Start Backend Server

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start server
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Verify Backend**:

```bash
# Health check
curl http://localhost:8001/health

# Check new chat endpoint exists
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"message": "hello", "conversation_id": null}'

# Should return 401 if no token, or chat response if valid token
```

---

## Step 5: Start Frontend

```bash
cd frontend

# Start development server
npm run dev
```

**Verify Frontend**:

1. Open browser: http://localhost:3000
2. Log in with Better Auth
3. Navigate to chat page: http://localhost:3000/chat
4. Should see chat interface

---

## Step 6: Validation Checklist

### Phase II Compatibility (No Breaking Changes)

- [ ] Existing task list UI still works
- [ ] Can create tasks via traditional UI
- [ ] Can complete tasks via traditional UI
- [ ] Can delete tasks via traditional UI
- [ ] REST API endpoints unchanged (`GET /api/{user_id}/tasks`, etc.)

### Phase III Chat Functionality

#### User Story 1: Natural Language Task Creation (P1)

- [ ] Open chat interface
- [ ] Type: "add a task to buy groceries tomorrow"
- [ ] Verify: Assistant responds with confirmation
- [ ] Verify: Task appears in traditional task list UI
- [ ] Verify: Task has correct title and due date

**Test Cases**:
```
Input: "remind me to call the dentist"
Expected: Task created with title "call the dentist", no due date

Input: "add task to finish report by Friday"
Expected: Task created with title "finish report", due date = upcoming Friday

Input: "I need to submit invoice by end of month"
Expected: Task created with appropriate title and due date
```

#### User Story 2: Conversational Task Management (P2)

- [ ] Type: "what are my tasks?"
- [ ] Verify: Assistant lists tasks
- [ ] Type: "complete the grocery task"
- [ ] Verify: Task marked as completed in both chat and UI
- [ ] Type: "show me overdue tasks"
- [ ] Verify: Filtered list returned

**Test Cases**:
```
Input: "what tasks do I have?"
Expected: List of user's tasks displayed

Input: "mark the first one as done"
Expected: First task from previous list marked completed

Input: "change the deadline for the report to next Monday"
Expected: Task due date updated

Input: "delete the dentist appointment"
Expected: Task deleted after confirmation
```

#### User Story 3: Conversation Persistence (P3)

- [ ] Create tasks in conversation
- [ ] Close chat page
- [ ] Reopen chat page
- [ ] Verify: Previous conversation history visible
- [ ] Type new message
- [ ] Verify: Conversation continues with context

---

## Step 7: Security Validation

### JWT Enforcement

```bash
# Test chat endpoint without JWT
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "conversation_id": null}'

# Should return: 401 Unauthorized
```

### Multi-User Isolation

1. Log in as User A
2. Create task via chat: "add task to buy milk"
3. Note task ID from response
4. Log out
5. Log in as User B
6. Try to access User A's task via chat: "complete task 123"
7. Verify: Assistant says task not found (doesn't reveal existence)

### User Identity from JWT Only

**Code Review Checklist**:
- [ ] MCP tools receive user_id from closure, not parameters
- [ ] Chat endpoint extracts user_id from JWT via `get_current_user` dependency
- [ ] No user_id in ChatRequest schema
- [ ] All database queries filter by user_id from JWT

---

## Step 8: Performance Validation

### Response Time

```bash
# Test chat response time
time curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <jwt-token>" \
  -d '{"message": "what are my tasks?", "conversation_id": null}'

# Should complete in < 3 seconds (SC-003)
```

### Concurrent Sessions

Use load testing tool (e.g., `ab`, `wrk`, `locust`):

```bash
# Install Apache Bench
# Ubuntu: sudo apt-get install apache2-utils
# macOS: brew install ab

# Test 100 concurrent requests
ab -n 100 -c 10 -H "Authorization: Bearer <jwt-token>" \
   -p chat-request.json -T application/json \
   http://localhost:8001/api/chat
```

Target: 100 concurrent sessions without degradation (SC-010)

---

## Step 9: Error Handling Validation

### AI Service Unavailable

1. Stop OpenAI API access (invalid API key or network block)
2. Send chat message
3. Verify: Graceful error message returned
4. Verify: User can still use traditional UI

**Expected Response**:
```json
{
  "conversation_id": "...",
  "message": {
    "role": "assistant",
    "content": "I'm having trouble connecting to my AI service right now. Please try again in a moment, or use the task list above to manage your tasks directly."
  },
  "error": "ai_service_unavailable"
}
```

### Database Error

Simulate database connection issue and verify graceful handling.

---

## Step 10: Stateless Validation

### Server Restart Test

1. Start conversation and create task via chat
2. Note conversation_id
3. Restart backend server (Ctrl+C, then restart)
4. Send new message with same conversation_id
5. Verify: Conversation continues (history loaded from DB)
6. Verify: No state lost

**This validates**:
- MCP tools are stateless (no in-memory state)
- Conversation context loaded from database
- Backend remains stateless per constitution

---

## Troubleshooting

### Chat Endpoint Returns 500

**Check**:
- OpenAI API key is valid
- OpenAI API has sufficient quota
- Database connection working
- Backend logs for detailed error

```bash
# Check backend logs
tail -f backend/logs/app.log

# Or if using uvicorn directly, check console output
```

### Tasks Not Appearing in UI

**Check**:
- Task created with correct user_id (from JWT)
- Frontend refreshing task list after chat action
- Database query filtering by user_id

```bash
# Check database directly
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE user_id = '<user-uuid>';"
```

### Conversation History Not Loading

**Check**:
- Conversation exists in database
- Conversation owned by authenticated user
- Messages table has records for conversation_id

```bash
# Check conversations
psql $DATABASE_URL -c "SELECT * FROM conversations WHERE user_id = '<user-uuid>';"

# Check messages
psql $DATABASE_URL -c "SELECT * FROM messages WHERE conversation_id = '<conv-uuid>';"
```

### Fuzzy Task Matching Not Working

**Check**:
- rapidfuzz installed correctly
- Task titles in database match expected format
- Matching threshold (70) is appropriate

**Debug**:
```python
from rapidfuzz import fuzz

# Test matching
score = fuzz.WRatio("buy groceries", "grocery shopping")
print(score)  # Should be > 70 for match
```

---

## Success Criteria Validation

After completing all steps, verify success criteria from spec.md:

- [ ] **SC-001**: Task creation <10 seconds from opening chatbot
- [ ] **SC-002**: 90% of simple requests interpreted correctly
- [ ] **SC-003**: Chat response time <3 seconds
- [ ] **SC-004**: Tasks from chat visible in UI immediately
- [ ] **SC-005**: Tasks from UI accessible via chat
- [ ] **SC-006**: Conversation history retained (check after 1 day)
- [ ] **SC-007**: All CRUD operations work via natural language
- [ ] **SC-008**: Zero breaking changes to Phase II APIs
- [ ] **SC-009**: Graceful AI service fallback
- [ ] **SC-010**: 100 concurrent sessions supported

---

## Next Steps

Once validation passes:

1. **Run Full Test Suite**:
   ```bash
   cd backend
   pytest tests/test_chat_api.py
   pytest tests/test_mcp_tools.py
   pytest tests/test_ai_agent.py
   ```

2. **Create Pull Request**:
   - Reference spec: `specs/003-ai-chatbot-mcp/spec.md`
   - Include validation checklist results
   - Note any deviations from plan

3. **Deploy to Staging**:
   - Verify environment variables set
   - Run database migrations
   - Smoke test all user stories

4. **Monitor Production**:
   - OpenAI API usage and costs
   - Chat response times
   - Error rates
   - User adoption metrics

---

## Rollback Plan

If Phase III causes issues:

1. **Revert Database Migration**:
   ```bash
   alembic downgrade -1
   ```

2. **Remove Chat UI**:
   - Remove `/chat` route from frontend
   - Users can still use traditional UI

3. **Disable Chat Endpoint**:
   - Comment out chat route in `backend/src/main.py`
   - Phase II functionality unaffected

**Phase II remains fully functional** - chat is additive only.

---

## Support

- **Spec**: `specs/003-ai-chatbot-mcp/spec.md`
- **Plan**: `specs/003-ai-chatbot-mcp/plan.md`
- **Data Model**: `specs/003-ai-chatbot-mcp/data-model.md`
- **API Contracts**: `specs/003-ai-chatbot-mcp/contracts/`
- **Constitution**: `.specify/memory/constitution.md`
