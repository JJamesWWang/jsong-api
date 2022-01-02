from jsong.member import Member


def context(members: dict[str, Member]):
    return {
        "event": "context",
        "payload": list(map(lambda m: m.dict(exclude={"websocket"}), members.values())),
    }


def connected(member: Member):
    return {"event": "connected", "payload": member.dict(exclude={"websocket"})}
