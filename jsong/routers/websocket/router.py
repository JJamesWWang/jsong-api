from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jsong.models.member import connect, Member
from jsong.routers.websocket import messages

router = APIRouter()
members: dict[str, Member] = {}


@router.websocket("/ws/{username}")
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
