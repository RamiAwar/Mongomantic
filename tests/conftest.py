import pytest
from mongomantic import connect


@pytest.fixture(scope="module")
def mongodb():
    connect("localhost:27017", "test", mock=True)