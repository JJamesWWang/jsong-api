from fastapi.testclient import TestClient
from websocket import router


client = TestClient(router)


def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_json()
        assert data["type"] == "connected"
        assert len(data["uid"]) > 0
