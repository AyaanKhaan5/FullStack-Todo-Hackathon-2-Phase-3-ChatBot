"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.database import create_db_and_tables

# Routers
from src.api.routes import auth, tasks, chat


# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Full-Stack Todo API",
    description="RESTful API for multi-user todo task management with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",  # explicit (frontend tools ke liye useful)
)


# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, PATCH
    allow_headers=["*"],  # Authorization, Content-Type, etc
)


# -----------------------------------------------------------------------------
# Startup
# -----------------------------------------------------------------------------
@app.on_event("startup")
async def on_startup() -> None:
    """
    Initialize database tables on application startup.
    """
    if settings.DEBUG:
        create_db_and_tables()


# -----------------------------------------------------------------------------
# Health Check
# -----------------------------------------------------------------------------
@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "todo-api"
    }


# -----------------------------------------------------------------------------
# Routers
# -----------------------------------------------------------------------------
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)


# -----------------------------------------------------------------------------
# Local Development Entry
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",   # 🔥 IMPORTANT (path fix)
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
    )
