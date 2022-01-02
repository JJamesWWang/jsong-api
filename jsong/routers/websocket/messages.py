from jsong.member import Member


def connected(member: Member):
    return {"event": "connected", "payload": member.dict(exclude={"websocket"})}
