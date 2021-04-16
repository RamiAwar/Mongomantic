from mongomantic import BaseRepository

from .user import User


class UserRepository(BaseRepository):
    class Meta:
        model = User
        collection = "user"
