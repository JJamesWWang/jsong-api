from fastapi import WebSocket
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Connection:
    websocket: WebSocket
    uid: str

    def __hash__(self):
        return hash(self.uid)

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Connection) and self.uid == __o.uid


def _gen_uid():
    return str(uuid4())


async def connect(connections: set[Connection], websocket: WebSocket) -> Connection:
    await websocket.accept()
    while (c := Connection(websocket, _gen_uid())) in connections:
        c = Connection(websocket, _gen_uid())
    return c
