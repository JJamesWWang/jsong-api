from fastapi import WebSocket
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class User:
    websocket: WebSocket
    uid: str
    username: str = ""

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, User) and self.uid == __o.uid


def _gen_uid():
    return str(uuid4())


class UserManager:
    def __init__(self):
        self.users: set[User] = set()

    async def connect(self, websocket: WebSocket) -> User:
        await websocket.accept()
        while (uid := _gen_uid()) in self.users:
            uid = _gen_uid()
        user = User(websocket, uid)
        self.users.add(user)
        return user

    def disconnect(self, user: User) -> None:
        self.users.discard(user)

    async def send_client(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for user in self.users:
            await user.websocket.send_text(message)
