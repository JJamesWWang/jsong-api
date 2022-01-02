from fastapi.testclient import TestClient
from jsong.routers.websocket.router import router


client = TestClient(router)


def test_websocket_context():
    with client.websocket_connect("/ws/hey") as websocket1:
        message = websocket1.receive_json()
        assert message["event"] == "context"
        context = message["payload"]
        assert len(context) == 0
        with client.websocket_connect("/ws/hi") as websocket2:
            message = websocket2.receive_json()
            assert message["event"] == "context"
            context = message["payload"]
            assert len(context) == 1
            with client.websocket_connect("/ws/what") as websocket3:
                message = websocket3.receive_json()
                assert message["event"] == "context"
                context = message["payload"]
                assert len(context) == 2


def test_websocket_connect():
    with client.websocket_connect("/ws/hey") as websocket:
        context = websocket.receive_json()
        message = websocket.receive_json()
        assert message["event"] == "connected"
        payload = message["payload"]
        assert len(payload["uid"]) > 0
        assert payload["username"] == "hey"
        assert payload["is_host"] is False
