from fastapi.testclient import TestClient
import pytest
from jsong.main import app


client = TestClient(app)


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


def test_game_starts_only_if_playlist_set():
    response = client.post("/lobby/start")
    assert response.status_code == 400


def test_set_playlist():
    response = client.put(
        "/lobby/playlist/",
        json={
            "link": "https://open.spotify.com/playlist/7Ia4x1WOfXZEwx8LvpleFI?si=1e046cac7db04acd"
        },
    )
    assert response.status_code == 200


def test_set_invalid_playlist():
    response = client.put(
        "/lobby/playlist/", json={"link": "https://youtube.com/watch?v=dQw4w9WgXcQ"}
    )
    assert response.status_code == 400
