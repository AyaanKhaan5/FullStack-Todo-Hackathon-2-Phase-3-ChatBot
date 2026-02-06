# Backend Setup Instructions

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment tool (venv)

## Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your configuration:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: Secret key for JWT token validation
   - `ALLOWED_ORIGINS`: Frontend URL (http://localhost:3000 for development)
   - `PORT`: Backend port (8001)
   - `DEBUG`: Set to True for development

## Running the Server

**Development mode** (with auto-reload):
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Production mode**:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8001
```

## API Documentation

Once the server is running, access:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc
- Health check: http://localhost:8001/health

## Project Structure

```
backend/
├── src/
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection and session
│   ├── models/           # SQLModel entities
│   │   ├── user.py       # User model
│   │   └── task.py       # Task model
│   ├── schemas/          # Pydantic request/response schemas
│   │   ├── user.py       # User schemas
│   │   └── task.py       # Task schemas
│   ├── middleware/       # Middleware components
│   │   └── auth.py       # JWT verification
│   └── api/              # API routes
│       ├── dependencies.py  # Dependency injection
│       └── routes/
│           └── tasks.py  # Task CRUD endpoints
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── .env.example         # Environment template
```

## Testing

Run tests with pytest:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

## Troubleshooting

**Port already in use**:
```bash
# Find process using port 8001
lsof -i :8001  # macOS/Linux
netstat -ano | findstr :8001  # Windows

# Kill the process or use a different port
```

**Database connection errors**:
- Verify DATABASE_URL is correct
- Check Neon PostgreSQL dashboard
- Ensure SSL mode is set: `sslmode=require`

**Import errors**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
