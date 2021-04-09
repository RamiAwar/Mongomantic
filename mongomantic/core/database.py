# # Package # #
from mongomantic.config import MongoSettings
from pymongo import MongoClient

__all__ = ["client", "db"]


class MongomanticClient:
    client = None
    db = None


def connect(uri: str, database: str, mock=False):
    if mock:
        try:
            import mongomock
        except ImportError:
            raise RuntimeError("Mongomock needs to be installed for mocking a connection")

        MongomanticClient.client = mongomock.MongoClient(uri)
    else:
        MongomanticClient.client = MongoClient(uri)

    MongomanticClient.db = MongomanticClient.client.__getattr__(database)
