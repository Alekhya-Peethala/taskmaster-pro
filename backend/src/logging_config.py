"""
TaskMaster Pro - Logging Configuration
Generated with GitHub Copilot assistance
Centralized logging setup for backend application
Supports development and production logging configurations
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """
    Configure application logging with console and optional file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs to console only.
    
    Usage in main.py:
        from src.logging_config import setup_logging
        setup_logging(log_level="INFO", log_file="logs/taskmaster.log")
    """
    # Get log level from environment or use provided default
    level = os.getenv("LOG_LEVEL", log_level).upper()
    numeric_level = getattr(logging, level, logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers to avoid duplicates
    root_logger.handlers = []
    
    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler (always enabled)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Rotating file handler (max 10MB, keep 5 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(log_format)
        root_logger.addHandler(file_handler)
    
    # Configure third-party loggers
    # Reduce SQLAlchemy verbosity in production
    if numeric_level > logging.DEBUG:
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    
    # Reduce uvicorn access logs in production
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    
    root_logger.info(f"Logging configured at {level} level")


# Configure logging on module import for development
# In production, call setup_logging() explicitly in main.py
if os.getenv("ENV", "development") == "development":
    setup_logging(log_level="DEBUG")
