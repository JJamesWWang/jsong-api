from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from jsong.routers.websocket.connection import connect, Connection
from jsong.routers.websocket.user import User
from jsong.routers.websocket import messages

router = APIRouter()
connections: dict[str, Connection] = {}
users: dict[str, User] = {}


@router.websocket("/ws")
async def get(websocket: WebSocket):
    connection = await connect(connections, websocket)
    connections[connection.uid] = connection
    await connection.websocket.send_json(messages.connected(connection))


@router.get("/ws/{uid}/{username}")
async def auth(uid: str, username: str):
    connection = connections.pop(uid, None)
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    users[uid] = User(connection, username)
    await listen_for_messages(users[uid])


async def listen_for_messages(user: User):
    try:
        while True:
            data = await user.websocket.receive_json()
    except WebSocketDisconnect:
        users.pop(user, None)
