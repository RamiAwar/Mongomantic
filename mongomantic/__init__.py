# type: ignore[attr-defined]
"""A MongoDB Python ORM, built on Pydantic and PyMongo."""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"


from mongomantic.core.base_repository import BaseRepository
from mongomantic.core.database import connect
from mongomantic.core.mongo_model import MongoDBModel

__all__ = ["BaseRepository", "MongoDBModel", "connect"]
