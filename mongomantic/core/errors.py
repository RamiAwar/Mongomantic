__all__ = [
    "WriteError",
    "InvalidQueryError",
    "DoesNotExistError",
    "MultipleObjectsReturnedError",
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
