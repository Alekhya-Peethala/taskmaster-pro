"""
TaskMaster Pro - Unit Tests for Logging Configuration
Generated with GitHub Copilot assistance
Test-Driven Development: Validate logging setup utility (Principle II)
"""

import logging
import os
import tempfile
import pytest
from src.logging_config import setup_logging


class TestSetupLogging:
    """Tests for the setup_logging() utility function."""

    def test_setup_logging_info_level(self):
        """setup_logging() configures the root logger at INFO level."""
        setup_logging(log_level="INFO")
        root = logging.getLogger()
        assert root.level == logging.INFO

    def test_setup_logging_debug_level(self):
        """setup_logging() configures the root logger at DEBUG level."""
        setup_logging(log_level="DEBUG")
        root = logging.getLogger()
        assert root.level == logging.DEBUG

    def test_setup_logging_warning_level(self):
        """setup_logging() configures the root logger at WARNING level."""
        setup_logging(log_level="WARNING")
        root = logging.getLogger()
        assert root.level == logging.WARNING

    def test_setup_logging_adds_console_handler(self):
        """setup_logging() attaches at least one StreamHandler."""
        setup_logging(log_level="INFO")
        root = logging.getLogger()
        handler_types = [type(h).__name__ for h in root.handlers]
        assert "StreamHandler" in handler_types

    def test_setup_logging_with_log_file(self):
        """setup_logging() creates a RotatingFileHandler when log_file is given."""
        with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as tmp:
            log_file = tmp.name

        try:
            setup_logging(log_level="INFO", log_file=log_file)
            root = logging.getLogger()
            handler_types = [type(h).__name__ for h in root.handlers]
            assert "RotatingFileHandler" in handler_types
        finally:
            # Cleanup: close file handlers to release the file lock
            for h in root.handlers[:]:
                if hasattr(h, "baseFilename") and h.baseFilename == log_file:
                    h.close()
                    root.removeHandler(h)
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_setup_logging_creates_log_directory(self):
        """setup_logging() creates parent directories for the log file if needed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = os.path.join(tmpdir, "subdir", "app.log")
            setup_logging(log_level="INFO", log_file=log_file)

            assert os.path.isdir(os.path.dirname(log_file))

            # Cleanup handlers
            root = logging.getLogger()
            for h in root.handlers[:]:
                if hasattr(h, "baseFilename") and h.baseFilename == log_file:
                    h.close()
                    root.removeHandler(h)

    def test_setup_logging_env_override(self, monkeypatch):
        """setup_logging() respects the LOG_LEVEL environment variable."""
        monkeypatch.setenv("LOG_LEVEL", "ERROR")
        setup_logging(log_level="DEBUG")  # env var should override
        root = logging.getLogger()
        assert root.level == logging.ERROR
