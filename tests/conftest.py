import pytest
from mongomantic import connect, disconnect


@pytest.fixture()
def mongodb():
    connect("localhost:27017", "test", mock=True)
    yield
    disconnect()
