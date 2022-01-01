from fastapi.testclient import TestClient
from jsong.routers.websocket.router import router


client = TestClient(router)


def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data["event"] == "connected"
        assert len(data["uid"]) > 0
