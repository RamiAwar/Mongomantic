from mongomantic.core.mongo_model import MongoDBModel


class User(MongoDBModel):

    first_name: str
    last_name: str
    email: str
    age: int
