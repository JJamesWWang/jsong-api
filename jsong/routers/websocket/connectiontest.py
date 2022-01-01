from jsong.routers.websocket.connection import Connection
import pytest


@pytest.fixture
def connection1():
    return Connection(websocket=None, uid="1")


@pytest.fixture
def connection2():
    return Connection(websocket=None, uid="2")


def test_equal_connection(connection1: Connection):
    assert connection1 == Connection(websocket=None, uid="1")


def test_unequal_connection(connection1: Connection, connection2: Connection):
    assert connection1 != connection2
