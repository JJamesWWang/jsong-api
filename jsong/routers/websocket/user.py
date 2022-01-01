from dataclasses import dataclass
from jsong.routers.websocket.connection import Connection


@dataclass
class User(Connection):
    username: str
    is_host: bool = False
