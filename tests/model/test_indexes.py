import pytest
from mongomantic import BaseRepository, Index, MongoDBModel
from mongomantic.core.errors import WriteError


class User(MongoDBModel):
    name: str
    email: str
    age: int


@pytest.fixture()
def repo():
    class UserRepository(BaseRepository):
        class Meta:
            model = User
            collection = "user"

            indexes = [
                Index(name="email_index", unique=True, fields=["+email"]),
                Index(name="name_age", unique=True, fields=["+age", "-name"]),
            ]

    return UserRepository


def test_index_creation(mongodb, repo):
    indexes = repo._get_collection().index_information()

    assert indexes["email_1"]["unique"]
    assert indexes["email_1"]["key"] == [("email", 1)]

    assert indexes["age_1_name_-1"]["unique"]
    assert indexes["age_1_name_-1"]["key"] == [("age", 1), ("name", -1)]


def test_index_duplicate_user(mongodb, repo):
    user = User(name="John", age=23, email="john@mail.com")
    repo.save(user)

    with pytest.raises(WriteError):
        repo.save(user)


def test_index_duplicate_email(mongodb, repo):
    user = User(name="John", age=23, email="john@mail.com")
    repo.save(user)

    same_email_user = User(name="John", age=2, email="john@mail.com")
    with pytest.raises(WriteError):
        repo.save(same_email_user)


def test_index_duplicate_name_age(mongodb, repo):
    user = User(name="John", age=23, email="john@mail.com")
    repo.save(user)

    similar_user = User(name="John", age=23, email="otherjohn@mail.com")
    with pytest.raises(WriteError):
        repo.save(similar_user)


def test_index_different_user(mongodb, repo):
    user = User(name="John", age=23, email="john@mail.com")
    repo.save(user)

    ok_user = User(name="John", age=30, email="otherotherjohn@mail.com")
    assert repo.save(ok_user)
