import logging
import os
from logging.handlers import RotatingFileHandler


class SafeRotatingFileHandler(RotatingFileHandler):
    """Handler that handles errors when writing to the log file"""

    def emit(self, record):
        try:
            return super().emit(record)
        except (PermissionError, OSError) as e:
            st_mode = oct(os.stat(self.baseFilename).st_mode)
            exists = os.path.exists(self.baseFilename)
            error_msg = (
                f"Failed to write to log file '{self.baseFilename}': "
                f"Error type: {type(e).__name__}, "
                f"Description: {e.strerror}, "
                f"Error code: {e.errno}, "
                f"File permissions: {st_mode if exists else 'File does not exist'}"
            )
            logging.error(error_msg)
            raise


class SafeFormatter(logging.Formatter):
    def format(self, record):
        try:
            return super().format(record)
        except (KeyError, ValueError):
            for key, default in [
                ("user", "!MISSING_user!"),
                ("ip", "!MISSING_ip!"),
                ("request_id", "!MISSING_request_id!"),
                ("method", "!MISSING_method!"),
                ("path", "!MISSING_path!"),
                ("status_code", "!MISSING_status_code!"),
                ("duration", 0.0),
            ]:
                if not hasattr(record, key):
                    setattr(record, key, default)
            return super().format(record)


class MaxLevelFilter(logging.Filter):
    """Allows only messages with a level lower than the specified one (exclusive)."""

    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        return record.levelno < self.max_level
