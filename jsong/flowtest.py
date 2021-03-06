from fastapi.testclient import TestClient
from fastapi import WebSocket
import pytest
import asyncio
from jsong.audio.playlist import Track
from jsong.main import app
from jsong.member import Member
from jsong.player import Player
from jsong.game import GameSettings


client = TestClient(app)


def receive_context(ws1: WebSocket, ws2: WebSocket):
    c1 = ws1.receive_json()
    c2 = ws2.receive_json()
    return c1, c2


def receive_connected(ws1: WebSocket, ws2: WebSocket):
    member1 = ws1.receive_json()["payload"]
    ws1.receive_json()  # ws2 connected also received
    member2 = ws2.receive_json()["payload"]
    return member1, member2


def receive_transfer_host(ws1: WebSocket, ws2: WebSocket):
    host = ws1.receive_json()["payload"]
    ws2.receive_json()  # should be same
    return host


def receive_start_game(ws1: WebSocket, ws2: WebSocket):
    state = ws1.receive_json()["payload"]
    ws2.receive_json()  # should be same
    return state


def receive_downloading_track(ws1: WebSocket, ws2: WebSocket):
    ws1.receive_json()
    ws2.receive_json()


def receive_next_round(ws1: WebSocket, ws2: WebSocket):
    ws1.receive_json()
    ws2.receive_json()


def send_ready(member1: dict, member2: dict):
    client.post(f"/lobby/ready/{member1['uid']}")
    client.post(f"/lobby/ready/{member2['uid']}")


def receive_start_round(ws1: WebSocket, ws2: WebSocket):
    ws1.receive_json()
    ws2.receive_json()


def receive_message(ws1: WebSocket, ws2: WebSocket):
    message = ws1.receive_json()
    ws2.receive_json()
    if message["event"] == "chat":
        return receive_chat(message)
    elif message["event"] == "correct_guess":
        return receive_correct_guess(message)


def receive_chat(message):
    member = message["payload"]["member"]
    chat = message["payload"]["content"]
    return member, chat


def receive_correct_guess(message):
    return message["payload"]


def receive_end_round(ws1: WebSocket, ws2: WebSocket):
    track: Track = ws1.receive_json()["payload"]
    ws2.receive_json()
    return track


def receive_end_game(ws1: WebSocket, ws2: WebSocket):
    ws1.receive_json()
    ws2.receive_json()


async def set_up_game(ws1: WebSocket, ws2: WebSocket):
    receive_context(ws1, ws2)
    member1, member2 = receive_connected(ws1, ws2)
    client.put(f"/lobby/host/{member1['uid']}")
    host = receive_transfer_host(ws1, ws2)
    assert host["uid"] == member1["uid"]
    response = client.put(
        "/lobby/playlist",
        json={
            "link": "https://open.spotify.com/playlist/0mAgqUtF9rEbXuIGFlIK4I?si=f178e9ee6fd444f6"
        },
    )
    assert response.status_code == 200
    return member1, member2


def start_game(host_uid: str):
    return asyncio.to_thread(client.post, f"/lobby/start/{host_uid}")


async def play_game(ws1: WebSocket, ws2: WebSocket, member1: dict, member2: dict):
    state = receive_start_game(ws1, ws2)
    assert len(state["players"]) == 2
    assert state["settings"]["playlistName"] == "Test Playlist"

    tracks = ["GLASSY", "Electric Shock", "D-D-DANCE"]

    await round1(ws1, ws2, member1, member2, tracks)
    await round2(ws1, ws2, member1, member2, tracks)
    await round3(ws1, ws2, member1, member2, tracks)

    receive_end_game(ws1, ws2)


async def round1(ws1, ws2, member1, member2, tracks):
    receive_downloading_track(ws1, ws2)
    receive_next_round(ws1, ws2)
    send_ready(member1, member2)
    receive_start_round(ws1, ws2)
    await asyncio.sleep(GameSettings.start_round_delay + 1)
    track = receive_end_round(ws1, ws2)
    assert track["name"] in tracks


async def round2(ws1, ws2, member1, member2, tracks):
    receive_downloading_track(ws1, ws2)
    receive_next_round(ws1, ws2)
    send_ready(member1, member2)
    receive_start_round(ws1, ws2)
    await asyncio.sleep(GameSettings.start_round_delay + 1)
    ws1.send_json("glassy")
    ws1.send_json("electric shock")
    ws1.send_json("d-d-dance")
    count, member = find_correct_and_count(ws1, ws2)
    assert count == 1
    assert member["uid"] == member1["uid"]
    track = receive_end_round(ws1, ws2)
    assert track["name"] in tracks


async def round3(ws1, ws2, member1, member2, tracks):
    receive_downloading_track(ws1, ws2)
    receive_next_round(ws1, ws2)
    send_ready(member1, member2)
    receive_start_round(ws1, ws2)
    await asyncio.sleep(GameSettings.start_round_delay + 1)
    ws1.send_json("glassy")
    ws1.send_json("electric shock")
    ws1.send_json("d-d-dance")
    count, member = find_correct_and_count(ws1, ws2)
    assert count == 1
    assert member["uid"] == member1["uid"]

    ws2.send_json("glassy")
    ws2.send_json("electric shock")
    ws2.send_json("d-d-dance")
    count, member = find_correct_and_count(ws1, ws2)
    assert count == 1
    assert member["uid"] == member2["uid"]

    track = receive_end_round(ws1, ws2)
    assert track["name"] in tracks


def find_correct_and_count(ws1: WebSocket, ws2: WebSocket):
    res1 = receive_message(ws1, ws2)
    res2 = receive_message(ws1, ws2)
    res3 = receive_message(ws1, ws2)
    member = None
    count = 0
    for r in [res1, res2, res3]:
        if isinstance(r, dict):
            count += 1
            member = r
    return count, member


@pytest.mark.asyncio
async def test_game_flow():
    with client.websocket_connect("/ws/1") as ws1:
        with client.websocket_connect("/ws/2") as ws2:
            member1, member2 = await set_up_game(ws1, ws2)
            await asyncio.gather(
                start_game(member1["uid"]), play_game(ws1, ws2, member1, member2)
            )
