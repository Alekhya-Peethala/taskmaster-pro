"""
TaskMaster Pro - Unit Tests for logging_config module
Ensures logging setup runs without errors in various configurations.
"""

import logging
import os
import pytest


class TestSetupLogging:
    """Tests for setup_logging() function."""

    def test_setup_logging_default_level(self):
        """setup_logging() with default args should not raise."""
        from src.logging_config import setup_logging
        setup_logging(log_level="WARNING")  # Use WARNING to avoid noisy output
        root = logging.getLogger()
        assert root.level == logging.WARNING

    def test_setup_logging_debug_level(self):
        """setup_logging() should accept DEBUG level."""
        from src.logging_config import setup_logging
        setup_logging(log_level="DEBUG")
        root = logging.getLogger()
        assert root.level == logging.DEBUG

    def test_setup_logging_with_log_file(self, tmp_path):
        """setup_logging() with a log_file path should create a file handler."""
        from src.logging_config import setup_logging
        log_file = str(tmp_path / "logs" / "test.log")
        setup_logging(log_level="INFO", log_file=log_file)
        assert os.path.exists(os.path.dirname(log_file))
        # Clean up handlers to avoid interfering with other tests
        root = logging.getLogger()
        root.handlers = []

    def test_setup_logging_respects_env_log_level(self, monkeypatch):
        """setup_logging() should read LOG_LEVEL from environment."""
        from src.logging_config import setup_logging
        monkeypatch.setenv("LOG_LEVEL", "ERROR")
        setup_logging()
        root = logging.getLogger()
        assert root.level == logging.ERROR
