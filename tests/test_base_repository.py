from typing import Generator

import pytest
from mongomantic.core.database import connect
from mongomantic.core.errors import DoesNotExistError, InvalidQueryError, MultipleObjectsReturnedError

from .user import User
from .user_repository import UserRepository


@pytest.fixture()
def mongodb():
    connect("localhost:27017", "test", mock=True)


def test_repository_save(mongodb):
    user = User(first_name="John", last_name="Smith", email="john@google.com", age=29)

    user_repo = UserRepository()
    user = user_repo.save(user)

    assert user
    assert user.id
    assert user.first_name == "John"


@pytest.fixture()
def example_user(mongodb):
    user = User(first_name="John", last_name="Smith", email="john@google.com", age=29)

    user_repo = UserRepository()
    return user_repo.save(user)


def test_repository_get(example_user):

    user = UserRepository().get(age=example_user.age)
    assert user
    assert user.first_name == example_user.first_name


def test_repository_get_does_not_exist(mongodb):
    with pytest.raises(DoesNotExistError):
        user = UserRepository().get(age=1)


def test_repository_get_with_duplicate(mongodb):
    user_repo = UserRepository()

    user = User(first_name="John", last_name="Smith", email="john@google.com", age=29)
    user_repo.save(user)

    duplicate = User(first_name="John", last_name="Smith", email="john@google.com", age=29)
    user_repo.save(duplicate)

    with pytest.raises(MultipleObjectsReturnedError):
        res = user_repo.get(age=29)


def test_repository_find(example_user):
    users = UserRepository().find(first_name="John")

    assert isinstance(users, Generator)
    users_list = list(users)

    assert len(users_list) == 1
    assert isinstance(users_list[0], User)
    assert users_list[0].first_name == example_user.first_name


def test_repository_find_nonexistent(mongodb):
    users = UserRepository().find(first_name="X")

    assert isinstance(users, Generator)
    assert len(list(users)) == 0


def test_repository_find_invalid_filter(mongodb):
    users = UserRepository().find(first_name={"$tf": "test"})
    assert isinstance(users, Generator)

    with pytest.raises(InvalidQueryError):
        assert len(list(users)) == 0
