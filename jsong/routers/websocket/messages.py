from jsong.routers.websocket.connection import Connection


def connected(connection: Connection):
    return {"event": "connected", "uid": connection.uid}
