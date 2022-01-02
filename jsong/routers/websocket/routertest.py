from fastapi.testclient import TestClient
from jsong.routers.websocket.router import router


client = TestClient(router)


def test_websocket_endpoint():
    with client.websocket_connect("/ws/hey") as websocket:
        data = websocket.receive_json()
        assert data["event"] == "connected"
        payload = data["payload"]
        assert len(payload["uid"]) > 0
        assert payload["username"] == "hey"
        assert payload["is_host"] is False
