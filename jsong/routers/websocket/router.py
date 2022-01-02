from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jsong.member import connect, Member
from jsong.routers.websocket import messages

router = APIRouter()
members: dict[str, Member] = {}


@router.websocket("/ws/{username}")
async def get_websocket(websocket: WebSocket, username: str):
    member = await connect(members, websocket, username)
    members[member.uid] = member
    await broadcast(messages.connected(member))
    await listen_for_messages(member)


async def broadcast(data: dict):
    for member in members.values():
        await member.websocket.send_json(data)


async def listen_for_messages(member: Member):
    try:
        while True:
            data = await member.websocket.receive_json()
    except WebSocketDisconnect:
        members.pop(member.uid, None)
