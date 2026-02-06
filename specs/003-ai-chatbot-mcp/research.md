# Research: AI-Powered Todo Chatbot with MCP

**Feature**: 003-ai-chatbot-mcp
**Date**: 2026-01-15
**Status**: Completed

## Research Objectives

This document consolidates research findings for implementing Phase III AI chatbot with MCP architecture.

---

## 1. OpenAI Agents SDK Integration

### Decision: Use OpenAI Agents SDK with Swarm Pattern

**Rationale**:
- OpenAI Agents SDK provides built-in support for tool calling and function execution
- Swarm pattern enables lightweight, multi-agent orchestration
- Native integration with MCP tools through function calling interface
- Supports streaming responses for better UX

**Implementation Approach**:
```python
from openai import OpenAI
from swarm import Swarm, Agent

# Initialize client
client = Swarm(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Define agent with MCP tools
task_agent = Agent(
    name="Task Manager",
    instructions="You help users manage their todo tasks through natural language.",
    functions=[add_task, list_tasks, complete_task, update_task, delete_task]
)

# Process user message
response = client.run(
    agent=task_agent,
    messages=conversation_history,
    context_variables={"user_id": user_id_from_jwt}
)
```

**Key Findings**:
- Context variables can pass JWT-derived user_id to all tool functions
- Agent instructions guide intent extraction and response generation
- Function calling automatically maps natural language to tool invocations
- Error handling through try-catch around client.run()

**Alternatives Considered**:
- LangChain: More complex, heavier dependencies
- Direct OpenAI API: Requires manual tool orchestration
- **Rejected because**: Agents SDK provides simpler integration with MCP tools

---

## 2. MCP Server Implementation

### Decision: Embedded MCP Server in FastAPI Process

**Rationale**:
- MCP tools run in same process as FastAPI backend
- Direct database access through existing SQLModel connection
- JWT context passed via function parameters
- No separate server process needed

**Implementation Approach**:
```python
# backend/src/mcp/server.py
from mcp import MCPServer

class TaskMCPServer:
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def create_tool_functions(self, user_id: str):
        """Create stateless tool functions with user context."""

        def add_task(title: str, description: str = None, due_date: str = None):
            """Stateless MCP tool - creates task in database."""
            with self.db_session_factory() as session:
                task = Task(
                    user_id=user_id,  # From JWT context
                    title=title,
                    description=description,
                    # ... parse due_date
                )
                session.add(task)
                session.commit()
                return task

        return [add_task, list_tasks, complete_task, update_task, delete_task]
```

**Key Findings**:
- Each request creates fresh tool functions with user_id closure
- Database session created per tool invocation (stateless)
- No in-memory state between requests
- Tools are pure functions: input → database operation → output

**Stateless Validation**:
- ✅ No class instance variables
- ✅ No module-level state
- ✅ Database session per invocation
- ✅ User context from parameters only

**Alternatives Considered**:
- Separate MCP server process: Added complexity, IPC overhead
- Stateful MCP server: Violates constitution Principle VII
- **Rejected because**: Embedded approach is simpler and maintains statelessness

---

## 3. ChatKit UI Integration

### Decision: Use @chatscope/chat-ui-kit-react

**Rationale**:
- Mature, well-documented React chat UI library
- Supports message bubbles, input, typing indicators
- Customizable styling with Tailwind CSS
- TypeScript support

**Implementation Approach**:
```tsx
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const { session } = useAuth(); // Better Auth session with JWT

  const handleSend = async (message: string) => {
    // Add user message to UI
    setMessages(prev => [...prev, { role: 'user', content: message }]);

    // Send to backend with JWT
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${session.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message, conversation_id: currentConversationId })
    });

    const data = await response.json();
    setMessages(prev => [...prev, data.message]);
  };

  return (
    <MainContainer>
      <ChatContainer>
        <MessageList>
          {messages.map(msg => (
            <Message
              model={{
                message: msg.content,
                sender: msg.role,
                direction: msg.role === 'user' ? 'outgoing' : 'incoming'
              }}
            />
          ))}
        </MessageList>
        <MessageInput onSend={handleSend} />
      </ChatContainer>
    </MainContainer>
  );
}
```

**Key Findings**:
- JWT token passed in Authorization header for each request
- Message state managed in React component
- Conversation history loaded on mount
- Real-time updates through state management (no WebSocket needed for MVP)

**Alternatives Considered**:
- Custom chat UI: More development time
- react-chat-elements: Less maintained
- **Rejected because**: @chatscope provides best balance of features and simplicity

---

## 4. Conversation Persistence

### Decision: PostgreSQL with Indexed Queries

**Database Schema**:
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    INDEX idx_conversations_user_id (user_id),
    INDEX idx_conversations_updated_at (updated_at)
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    INDEX idx_messages_conversation_id (conversation_id),
    INDEX idx_messages_created_at (created_at)
);
```

**Query Patterns**:
```python
# Get recent conversations for user
conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
    .limit(20)
).all()

# Get conversation history with pagination
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.asc())
    .offset(offset)
    .limit(50)
).all()
```

**Key Findings**:
- UUID primary keys for conversations and messages
- Cascade delete ensures cleanup when user deleted
- Indexes on user_id and conversation_id for fast lookups
- Pagination prevents loading entire conversation history
- 30-day retention enforced via scheduled cleanup job (out of scope for MVP)

**Performance Considerations**:
- Index on conversations.updated_at for "recent conversations" query
- Index on messages.created_at for chronological ordering
- Limit conversation history to last 100 messages per load
- Lazy loading for older messages

---

## 5. Task Matching & Fuzzy Search

### Decision: Use rapidfuzz Library

**Rationale**:
- Fast Levenshtein distance calculation
- Python 3.11+ compatible
- Better performance than fuzzywuzzy
- Simple API for string matching

**Implementation Approach**:
```python
from rapidfuzz import fuzz, process

def find_matching_task(user_input: str, user_tasks: List[Task], threshold: int = 70):
    """Find task matching user's natural language description."""

    # Extract task titles
    task_titles = {task.id: task.title for task in user_tasks}

    # Find best match
    result = process.extractOne(
        user_input,
        task_titles.values(),
        scorer=fuzz.WRatio,
        score_cutoff=threshold
    )

    if result:
        matched_title, score, _ = result
        # Find task by title
        task = next(t for t in user_tasks if t.title == matched_title)

        if score < 85:
            # Ambiguous match - ask for confirmation
            return {"task": task, "confidence": "low", "score": score}
        else:
            return {"task": task, "confidence": "high", "score": score}

    return None  # No match found
```

**Matching Strategy**:
- Score >= 85: High confidence, proceed with action
- Score 70-84: Low confidence, ask user to confirm
- Score < 70: No match, ask user to clarify

**Disambiguation Prompt**:
```
"I found a task that might match: '{task.title}'. Is this the one you meant?"
```

**Key Findings**:
- WRatio scorer handles partial matches well
- Threshold of 70 balances precision and recall
- Confirmation step prevents wrong task operations
- Multiple matches (score difference <10) trigger disambiguation

**Alternatives Considered**:
- Exact string matching: Too rigid for natural language
- Semantic search with embeddings: Overkill for task titles
- **Rejected because**: Fuzzy matching provides good balance

---

## 6. Error Handling & Fallback

### Decision: Graceful Degradation with User-Friendly Messages

**OpenAI API Unavailable**:
```python
try:
    response = client.run(agent=task_agent, messages=messages)
except OpenAIError as e:
    return {
        "message": {
            "role": "assistant",
            "content": "I'm having trouble connecting to my AI service right now. "
                      "Please try again in a moment, or use the task list above to manage your tasks directly."
        },
        "error": "ai_service_unavailable"
    }
```

**Rate Limit Exceeded**:
```python
except RateLimitError:
    return {
        "message": {
            "role": "assistant",
            "content": "I'm receiving too many requests right now. "
                      "Please wait a moment and try again."
        },
        "error": "rate_limit_exceeded"
    }
```

**Database Error**:
```python
except SQLAlchemyError as e:
    logger.error(f"Database error in chat: {e}")
    return {
        "message": {
            "role": "assistant",
            "content": "I encountered an error saving your request. "
                      "Please try again or contact support if the issue persists."
        },
        "error": "database_error"
    }
```

**Key Findings**:
- Always return valid response structure (never 500 errors to user)
- Log errors for debugging but show friendly messages
- Provide alternative action (use traditional UI)
- Include error codes for frontend handling

---

## 7. Security Considerations

### JWT Context Extraction

**Critical Pattern**:
```python
# backend/src/mcp/context.py
from fastapi import Depends, HTTPException
from backend.src.api.dependencies import get_current_user

async def extract_user_context(
    current_user: User = Depends(get_current_user)
) -> dict:
    """Extract user context from JWT for MCP tools."""
    return {
        "user_id": str(current_user.id),
        "email": current_user.email
    }

# In chat endpoint
@router.post("/chat")
async def chat(
    request: ChatRequest,
    user_context: dict = Depends(extract_user_context)
):
    # user_context["user_id"] is from JWT, never from request body
    mcp_tools = mcp_server.create_tool_functions(user_context["user_id"])
    # ...
```

**Security Validations**:
- ✅ User ID from JWT only (never from request.body or URL)
- ✅ MCP tools receive user_id as parameter (not from global state)
- ✅ Database queries filter by user_id (user ownership enforcement)
- ✅ No user_id in request body schema

---

## Summary of Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| AI Framework | OpenAI Agents SDK with Swarm | Native MCP integration, simpler than LangChain |
| MCP Architecture | Embedded in FastAPI | Stateless, direct DB access, no IPC overhead |
| Chat UI | @chatscope/chat-ui-kit-react | Mature, TypeScript support, customizable |
| Database | PostgreSQL with indexes | Existing Neon setup, efficient queries |
| Task Matching | rapidfuzz with WRatio | Fast, good for natural language matching |
| Error Handling | Graceful degradation | User-friendly messages, always valid responses |
| Security | JWT context extraction | User ID from token only, prevents spoofing |

---

## Open Questions Resolved

1. **How to pass JWT context to stateless MCP tools?**
   - Answer: Create tool functions with user_id closure per request

2. **How to handle conversation context in stateless backend?**
   - Answer: Load conversation history from database per request

3. **What threshold for fuzzy task matching?**
   - Answer: 70 minimum, 85+ for high confidence, confirmation for 70-84

4. **How to handle OpenAI API failures?**
   - Answer: Graceful fallback with user-friendly error messages

5. **Which chat UI library?**
   - Answer: @chatscope/chat-ui-kit-react for best balance

---

## Next Steps

1. Proceed to Phase 1: Create data-model.md with complete SQLModel schemas
2. Generate API contracts in contracts/ directory
3. Create quickstart.md with setup instructions
4. Begin implementation with Phase 2.1 (Foundation)
