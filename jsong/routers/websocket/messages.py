from user import User


def connected(user: User):
    return {"type": "connected", "uid": user.uid}
