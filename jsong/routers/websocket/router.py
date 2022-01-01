from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from user import UserManager
import messages

router = APIRouter()
user_manager = UserManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    user = await user_manager.connect(websocket)
    await websocket.send_json(messages.connected(user))
    try:
        while True:
            data = await websocket.receive_json()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        user_manager.disconnect(user)
        # await manager.broadcast(f"Client #{client_id} left the chat")
