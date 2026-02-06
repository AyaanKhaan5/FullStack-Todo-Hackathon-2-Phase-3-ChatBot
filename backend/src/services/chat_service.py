"""Chat service for orchestrating conversation flow."""
from sqlmodel import Session, select
from ..models.conversation import Conversation
from ..models.message import Message, MessageRole
from .ai_agent import AIAgent
from .task_service import TaskService
from ..mcp.server import TaskMCPServer
from ..mcp.tools.add_task import create_add_task_tool
from ..schemas.chat import ChatResponse, MessageResponse, ActionResponse
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class ChatService:
    """Service for chat operations and AI orchestration."""

    def __init__(
        self,
        session: Session,
        ai_agent: AIAgent,
        user_id: str
    ):
        """
        Initialize chat service.

        Args:
            session: Database session
            ai_agent: AI agent instance
            user_id: User ID from JWT
        """
        self.session = session
        self.ai_agent = ai_agent
        self.user_id = user_id
        self.user_uuid = uuid.UUID(user_id)

    def process_chat_message(
        self,
        message: str,
        conversation_id: Optional[uuid.UUID] = None
    ) -> ChatResponse:
        """
        Process chat message and return response.

        Args:
            message: User's message
            conversation_id: Existing conversation ID or None for new

        Returns:
            ChatResponse with assistant message and actions
        """
        # Get or create conversation
        if conversation_id:
            conversation = self._get_conversation(conversation_id)
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            conversation = self._create_conversation()

        # Save user message
        user_message = self._save_message(
            conversation.id,
            MessageRole.USER,
            message
        )

        # Load conversation history
        history = self._load_conversation_history(conversation.id)

        # Create MCP tools with user context
        task_service = TaskService(self.session)
        add_task_tool = create_add_task_tool(task_service, self.user_uuid)
        tools = [add_task_tool]

        # Process message with AI agent
        try:
            ai_response = self.ai_agent.process_message(
                message,
                history,
                tools
            )

            assistant_content = ai_response.get("content", "I'm not sure how to help with that.")

            # Save assistant message
            assistant_message = self._save_message(
                conversation.id,
                MessageRole.ASSISTANT,
                assistant_content
            )

            # Update conversation title if first message
            if not conversation.title:
                conversation.title = message[:50] + ("..." if len(message) > 50 else "")
                self.session.add(conversation)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()

            # Build actions list
            actions = []
            if ai_response.get("function_called") == "add_task":
                result = ai_response.get("function_result", {})
                actions.append(ActionResponse(
                    type="task_created",
                    task_id=result.get("id")
                ))

            return ChatResponse(
                conversation_id=conversation.id,
                message=MessageResponse(
                    id=assistant_message.id,
                    role=assistant_message.role.value,
                    content=assistant_message.content,
                    created_at=assistant_message.created_at
                ),
                actions=actions
            )

        except Exception as e:
            # Handle AI service errors gracefully
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"AI service error: {str(e)}", exc_info=True)

            error_message = "I'm having trouble connecting to my AI service right now. Please try again in a moment, or use the task list above to manage your tasks directly."

            assistant_message = self._save_message(
                conversation.id,
                MessageRole.ASSISTANT,
                error_message
            )

            self.session.commit()

            return ChatResponse(
                conversation_id=conversation.id,
                message=MessageResponse(
                    id=assistant_message.id,
                    role=assistant_message.role.value,
                    content=error_message,
                    created_at=assistant_message.created_at
                ),
                actions=[],
                error="ai_service_unavailable"
            )

    def _get_conversation(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """Get conversation by ID for the user."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_uuid
        )
        return self.session.exec(statement).first()

    def _create_conversation(self) -> Conversation:
        """Create new conversation for the user."""
        conversation = Conversation(
            user_id=self.user_uuid,
            title=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.session.add(conversation)
        self.session.flush()
        return conversation

    def _save_message(
        self,
        conversation_id: uuid.UUID,
        role: MessageRole,
        content: str
    ) -> Message:
        """Save message to database."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        self.session.add(message)
        self.session.flush()
        return message

    def _load_conversation_history(
        self,
        conversation_id: uuid.UUID
    ) -> List[Dict[str, str]]:
        """Load conversation history for AI context."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        messages = self.session.exec(statement).all()

        return [
            {
                "role": msg.role.value.lower(),  # Convert to lowercase for API
                "content": msg.content
            }
            for msg in messages
        ]
