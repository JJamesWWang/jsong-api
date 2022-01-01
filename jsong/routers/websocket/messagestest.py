from user import User
import messages
import pytest


@pytest.fixture
def user():
    return User(websocket=None, uid="1", username="K")


def test_connected(user: User):
    message = messages.connected(user)
    assert message["event"] == "connected"
    assert len(message["uid"]) > 0
