from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jsong.member import connect, Member
from jsong.audio.playlist import Playlist
from jsong.audio.spotify import get_playlist
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
    game: Game = None

    @classmethod
    def with_members(cls, state, members):
        return cls(members, state.playlist)


JSONG_STATE: GlobalState = GlobalState()


@app.websocket("/ws/{username}")
async def get_websocket(websocket: WebSocket, username: str):
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
    return


@app.post("/lobby/end", status_code=200)
async def end_game():
    await broadcast(messages.end_game())
