from jsong.routers.websocket.user import User


def connected(user: User):
    return {"event": "connected", "uid": user.uid}
