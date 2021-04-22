__all__ = [
    "WriteError",
    "InvalidQueryError",
    "DoesNotExistError",
    "MultipleObjectsReturnedError",
    "FieldDoesNotExistError",
]


class WriteError(Exception):
    pass


class InvalidQueryError(Exception):
    pass


class DoesNotExistError(Exception):
    pass


class MultipleObjectsReturnedError(Exception):
    pass


class FieldDoesNotExistError(Exception):
    pass


class IndexCreationError(Exception):
    pass


class DuplicateKeyError(Exception):
    pass
