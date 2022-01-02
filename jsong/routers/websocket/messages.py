from jsong.member import Member


def context(members: dict[str, Member]):
    return {
        "event": "context",
        "payload": list(map(lambda m: _json(m), members.values())),
    }


def _json(member: Member):
    return member.dict(exclude={"websocket"})


def connected(member: Member):
    return {"event": "connected", "payload": _json(member)}


def disconnected(member: Member):
    return {"event": "disconnected", "payload": _json(member)}


def chat(member: Member, content: str):
    return {
        "event": "chat",
        "payload": {
            "member": _json(member),
            "content": content,
        },
    }
