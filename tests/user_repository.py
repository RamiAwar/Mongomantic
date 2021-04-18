from mongomantic import BaseRepository
from mongomantic.utils.safe_repository import SafeRepository

from .user import User


class UserRepository(BaseRepository):
    class Meta:
        model = User
        collection = "user"


class SafeUserRepository(SafeRepository):
    class Meta:
        model = User
        collection = "user"
