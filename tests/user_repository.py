from mongomantic import BaseRepository

from .user import User


class UserRepository(BaseRepository):
    @property
    def _model(self):
        return User

    @property
    def _collection(self):
        return "user"
