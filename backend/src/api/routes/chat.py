"""Chat API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...database import get_session
from ...mcp.context import extract_user_context
from ...schemas.chat import ChatRequest, ChatResponse
from ...services.chat_service import ChatService
from ...services.ai_agent import AIAgent
from ...config import settings

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_context: dict = Depends(extract_user_context),
    session: Session = Depends(get_session)
):
    """
    Process chat message and return AI response.

    User identity is derived from JWT token only.
    """
    # Validate OpenAI API key is configured
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please set OPENAI_API_KEY."
        )

    # Initialize AI agent
    ai_agent = AIAgent(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL
    )

    # Initialize chat service
    chat_service = ChatService(
        session=session,
        ai_agent=ai_agent,
        user_id=user_context["user_id"]
    )

    # Process message
    try:
        response = chat_service.process_chat_message(
            message=request.message,
            conversation_id=request.conversation_id
        )
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )

