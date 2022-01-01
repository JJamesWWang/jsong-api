from fastapi.testclient import TestClient
from websocket import router


client = TestClient(router)


def test_websocket_endpoint():
    with client.websocket_connect("/ws") as websocket:
        assert websocket.receive_json()
