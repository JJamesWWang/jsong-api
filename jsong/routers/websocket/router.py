from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from jsong.routers.websocket.connection import connect, Connection
from jsong.routers.websocket.user import User
from jsong.routers.websocket import messages

router = APIRouter()
connections: set[Connection] = set()
users: set[User] = set()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    connection = await connect(connections, websocket)
    connections.add(connection)
    await websocket.send_json(messages.connected(connection))
    try:
        while True:
            data = await websocket.receive_json()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        connections.discard(connection)
        # await manager.broadcast(f"Client #{client_id} left the chat")
