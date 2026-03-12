"""
TaskMaster Pro - FastAPI Application Entry Point
Generated with GitHub Copilot assistance
Main application configuration with CORS middleware and route registration
Constitution: Azure-Native Architecture (Principle I), API Contract Compliance (Principle V)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application instance
app = FastAPI(
    title="TaskMaster Pro API",
    description="RESTful API for task management with CRUD operations and status filtering",
    version="1.0.0",
    docs_url="/api/docs",          # Swagger UI at /api/docs
    redoc_url="/api/redoc",         # ReDoc at /api/redoc
    openapi_url="/api/openapi.json" # OpenAPI schema at /api/openapi.json
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


# Application lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Performs initialization tasks when the app starts.
    """
    # TODO: Initialize database connection pool
    # TODO: Verify database connection
    # TODO: Run database migrations (if auto-migrate enabled)
    print("TaskMaster Pro API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Performs cleanup tasks when the app shuts down.
    """
    # TODO: Close database connections
    # TODO: Cleanup resources
    print("TaskMaster Pro API shutting down...")


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
