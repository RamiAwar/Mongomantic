import pytest
from mongomantic import BaseRepository, Index, MongoDBModel
from mongomantic.core.errors import WriteError


class User(MongoDBModel):
    name: str
    email: str
    age: int


class UserRepository(BaseRepository):
    class Meta:
        model = User
        collection = "user"

        indexes = [
            Index(name="email_index", unique=True, fields=["+email"]),
            Index(name="name_age", unique=True, fields=["+age", "-name"]),
        ]


def test_index_creation(mongodb):
    indexes = UserRepository._get_collection().index_information()

    assert indexes["email_1"]["unique"]
    assert indexes["email_1"]["key"] == [("email", 1)]

    assert indexes["age_1_name_-1"]["unique"]
    assert indexes["age_1_name_-1"]["key"] == [("age", 1), ("name", -1)]


def test_index_uniqueness(mongodb):
    user = User(name="John", age=23, email="john@mail.com")

    UserRepository.save(user)
    with pytest.raises(WriteError):
        UserRepository.save(user)

    same_email_user = User(name="John", age=2, email="john@mail.com")
    with pytest.raises(WriteError):
        UserRepository.save(same_email_user)

    similar_user = User(name="John", age=23, email="otherjohn@mail.com")
    with pytest.raises(WriteError):
        UserRepository.save(similar_user)

    ok_user = User(name="John", age=30, email="otherotherjohn@mail.com")
    assert UserRepository.save(ok_user)
