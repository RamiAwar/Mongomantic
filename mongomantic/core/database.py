# # Package # #
from pymongo import MongoClient
from pymongo.database import Database

__all__ = ["MongomanticClient"]


class MongomanticClient:
    client: MongoClient = None
    db: Database = None


def connect(uri: str, database: str, mock: bool = False) -> None:
    if mock:
        try:
            import mongomock
        except ImportError:
            raise RuntimeError("Mongomock needs to be installed for mocking a connection")
        MongomanticClient.client = mongomock.MongoClient(uri)
    else:
        MongomanticClient.client = MongoClient(uri)

    MongomanticClient.db = MongomanticClient.client.__getattr__(database)
