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
    await listen_for_messages(connection)


@router.get("/ws/{uid}/{username}")
async def auth(uid: str, username: str):
    connection = connections.pop(uid, None)
    if not connection:
        raise HTTPException(status_code=404, detail="Connection not found")
    users[uid] = User(connection, username)


async def listen_for_messages(connection: Connection):
    try:
        while True:
            data = await connection.websocket.receive_json()
    except WebSocketDisconnect:
        connections.pop(connection.uid, None)
        users.pop(connection.uid, None)
