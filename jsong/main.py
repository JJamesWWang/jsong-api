from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from toolz import dicttoolz
import asyncio
import random
from jsong.member import connect, Member
from jsong.audio.playlist import Playlist
from jsong.audio.spotify import get_playlist
from jsong.audio.downloader import download
from jsong.audio.audiosplicer import splice
from jsong.game import Game
import jsong.messages as messages

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GlobalState:  # my greatest mistake, but it works
    members: dict[str, Member] = {}
    playlist: Playlist = None
    game: Game = Game.empty()

    @classmethod
    def with_members(cls, state, members):
        return cls(members, state.playlist)


JSONG_STATE: GlobalState = GlobalState()


@app.websocket("/ws/{username}")
async def get_websocket(websocket: WebSocket, username: str):
    if JSONG_STATE.game.is_active:
        raise HTTPException(status_code=400, detail="Game is already in progress")
    members = JSONG_STATE.members
    member = await connect(members, websocket, username)
    await member.websocket.send_json(messages.context(members))
    members[member.uid] = member
    await broadcast(messages.connected(member))
    await listen_for_messages(member)


async def broadcast(data: dict):
    for member in JSONG_STATE.members.values():
        await member.websocket.send_json(data)


async def listen_for_messages(member: Member):
    try:
        while True:
            content = await member.websocket.receive_json()
            if JSONG_STATE.game.is_active and JSONG_STATE.game.guess(
                member.uid, content
            ):
                await broadcast(messages.correct_guess(member))
            else:
                await broadcast(messages.chat(member, content))
    except WebSocketDisconnect:
        JSONG_STATE.members.pop(member.uid, None)
        await broadcast(messages.disconnected(member))


@app.put("/lobby/host/{uid}", status_code=200)
async def claim_host(uid: str):
    if uid not in JSONG_STATE.members:
        raise HTTPException(status_code=404, detail="Member not found")
    JSONG_STATE.members = {
        m.uid: Member.with_host(m, m.uid == uid) for m in JSONG_STATE.members.values()
    }
    await broadcast(messages.transfer_host(JSONG_STATE.members[uid]))


class PlaylistLink(BaseModel):
    link: str


@app.put("/lobby/playlist/", status_code=200)
async def set_playlist(data: PlaylistLink):
    try:
        JSONG_STATE.playlist = get_playlist(data.link)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/lobby/start", status_code=200)
async def start_game():
    if not JSONG_STATE.playlist:
        raise HTTPException(status_code=400, detail="No playlist set")
    JSONG_STATE.game = Game(JSONG_STATE.members, JSONG_STATE.playlist)
    await broadcast(messages.start_game())
    await game_loop()
    await broadcast(messages.end_game())


async def game_loop():
    while JSONG_STATE.game.is_active:
        JSONG_STATE.game.advance_round()
        await broadcast(messages.downloading_track())
        splice_track()
        await broadcast(messages.next_round())
        await wait_until_players_ready()
        await broadcast(messages.start_round())
        await wait_until_track_done_playing()
        await broadcast(messages.end_round())


def splice_track():
    track = JSONG_STATE.game.current_track
    dtrack = download(track)
    start = random.randint(0, track.duration - JSONG_STATE.game.play_length)
    splice(dtrack, start, start + JSONG_STATE.game.play_length * 1000)


async def wait_until_players_ready():
    while not all(m.isReady for m in JSONG_STATE.members.values()):
        await asyncio.sleep(1)


@app.post("/lobby/ready/{uid}", status_code=200)
async def set_ready(uid: str):
    if uid not in JSONG_STATE.members:
        raise HTTPException(status_code=404, detail="Member not found")
    member = JSONG_STATE.members[uid]
    JSONG_STATE.members = dicttoolz.assoc(
        JSONG_STATE.members, uid, Member.with_isReady(member, True)
    )


async def wait_until_track_done_playing():
    for _ in range(JSONG_STATE.game.play_length):
        await asyncio.sleep(1)


@app.post("/lobby/end", status_code=200)
async def end_game():
    JSONG_STATE.game.rounds = float("inf")
    await broadcast(messages.end_game())
