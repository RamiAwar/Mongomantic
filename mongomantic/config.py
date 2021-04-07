import logging
import os

__all__ = ["MongoSettings", "logger"]


class MongoSettings:
    uri: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database: str = os.getenv("MONGO_DATABASE", "test")


class CleanFormatter(logging.Formatter):
    """Logging Formatter without colors"""

    fmt = "%(levelname)s:     %(message)s (%(filename)s:%(lineno)d) <%(funcName)s> @ %(asctime)s"

    def format(self, record):
        formatter = logging.Formatter(self.fmt)
        return formatter.format(record)


_channel_handler = logging.StreamHandler()
_channel_handler.setFormatter(CleanFormatter())

logger = logging.getLogger("mongomantic")
logger.addHandler(_channel_handler)
