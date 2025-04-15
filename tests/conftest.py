import pytest

HOST = "127.0.0.1"
PORT = 12345


@pytest.fixture
def host():
    return HOST


@pytest.fixture
def port():
    return PORT
