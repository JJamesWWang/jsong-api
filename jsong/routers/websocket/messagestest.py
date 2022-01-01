import messages


def test_connected():
    message = messages.connected()
    assert message["type"] == "connected"
