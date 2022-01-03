from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from jsong.member import connect, Member
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

members: dict[str, Member] = {}


@app.websocket("/ws/{username}")
async def get_websocket(websocket: WebSocket, username: str):
    member = await connect(members, websocket, username)
    await member.websocket.send_json(messages.context(members))
    members[member.uid] = member
    await broadcast(messages.connected(member))
    await listen_for_messages(member)


async def broadcast(data: dict):
    for member in members.values():
        await member.websocket.send_json(data)


async def listen_for_messages(member: Member):
    try:
        while True:
            content = await member.websocket.receive_json()
            await broadcast(messages.chat(member, content))
    except WebSocketDisconnect:
        members.pop(member.uid, None)
        await broadcast(messages.disconnected(member))


@app.put("/lobby/host/{uid}", status_code=200)
async def claim_host(uid: str):
    if uid not in members:
        raise HTTPException(status_code=404, detail="Member not found")
    for m in members.values():
        members[m.uid] = m.with_host(m.uid == uid)
    await broadcast(messages.transfer_host(members[uid]))


# @router.put("/lobby/playlist", status_code=200)
# async def set_playlist(playlist: str):
#     pass
