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
        assert payload["isHost"] is False


def test_websocket_disconnect():
    with client.websocket_connect("/ws/hey") as websocket1:
        with client.websocket_connect("/ws/hi") as websocket2:
            pass
        context = websocket1.receive_json()
        ws1_connected = websocket1.receive_json()
        ws2_connected = websocket1.receive_json()
        disconnected = websocket1.receive_json()
        payload = disconnected["payload"]
        assert payload["username"] == "hi"


def test_websocket_chat():
    with client.websocket_connect("/ws/hey") as websocket1:
        with client.websocket_connect("/ws/hi") as websocket2:
            websocket2.send_json("hello")
            context = websocket1.receive_json()
            ws1_connected = websocket1.receive_json()
            ws2_connected = websocket1.receive_json()
            chat = websocket1.receive_json()
            payload = chat["payload"]
            assert payload["member"]["username"] == "hi"
            assert payload["content"] == "hello"


def test_websocket_claim_host():
    with client.websocket_connect("/ws/hey") as websocket1:
        with client.websocket_connect("/ws/hi") as websocket2:
            context = websocket1.receive_json()
            ws1_connected = websocket1.receive_json()
            ws2_connected = websocket1.receive_json()
            client.put(f"/lobby/host/{ws2_connected['payload']['uid']}")
            claim_host = websocket1.receive_json()
            payload = claim_host["payload"]
            assert payload["username"] == "hi"
