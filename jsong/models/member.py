from fastapi import WebSocket
from dataclasses import dataclass
from uuid import uuid4
from pydantic import BaseModel


class Member(BaseModel):
    uid: str
    websocket: WebSocket
    username: str
    is_host: bool = False

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Member) and self.uid == __o.uid

    class Config:
        arbitrary_types_allowed = True


def _gen_uid():
    return str(uuid4())


async def connect(
    members: dict[str, Member], websocket: WebSocket, username: str
) -> Member:
    await websocket.accept()
    while (uid := _gen_uid()) in members:
        uid = _gen_uid()
    return Member(uid=uid, websocket=websocket, username=username)
