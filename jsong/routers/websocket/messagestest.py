from jsong.routers.websocket.connection import Connection
from jsong.routers.websocket import messages
import pytest


@pytest.fixture
def connection():
    return Connection(websocket=None, uid="1")


def test_connected(connection: Connection):
    message = messages.connected(connection)
    assert message["event"] == "connected"
    assert len(message["uid"]) > 0
