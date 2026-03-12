"""
TaskMaster Pro - FastAPI Application Entry Point
Generated with GitHub Copilot assistance
Main application configuration with CORS middleware and route registration
Constitution: Azure-Native Architecture (Principle I), API Contract Compliance (Principle V)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(application: FastAPI):
    """
    Application lifespan event handler.
    Handles startup and shutdown events using the modern lifespan pattern.
    """
    # Startup
    print("TaskMaster Pro API starting up...")
    yield
    # Shutdown
    print("TaskMaster Pro API shutting down...")


# Create FastAPI application instance
app = FastAPI(
    title="TaskMaster Pro API",
    description="RESTful API for task management with CRUD operations and status filtering",
    version="1.0.0",
    docs_url="/api/docs",           # Swagger UI at /api/docs
    redoc_url="/api/redoc",          # ReDoc at /api/redoc
    openapi_url="/api/openapi.json",  # OpenAPI schema at /api/openapi.json
    lifespan=lifespan,
)

# CORS Configuration
# Allow frontend origin for development and production
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:4200,http://localhost:3000"  # Default: Angular dev server
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register global exception handlers
from src.middleware.error_handler import register_exception_handlers
register_exception_handlers(app)


# Root health check endpoint
@app.get("/")
async def root():
    """
    Root endpoint for health checks.
    Returns application name and version.
    """
    return {
        "name": "TaskMaster Pro API",
        "version": "1.0.0",
        "status": "healthy"
    }


# Register API routers
from src.api import tasks
app.include_router(tasks.router, prefix="/api", tags=["tasks"])


if __name__ == "__main__":
    import uvicorn

    # Run the application with uvicorn
    # Development mode with auto-reload
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (disable in production)
        log_level="info"
    )
