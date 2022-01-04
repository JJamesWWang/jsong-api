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


def transfer_host(member: Member):
    return {
        "event": "transfer_host",
        "payload": _json(member),
    }


def start_game():
    return {"event": "start_game", "payload": {}}


def next_round():
    return {"event": "next_round", "payload": {}}


def start_round():
    return {"event": "start_round", "payload": {}}


def correct_guess(member: Member):
    return {"event": "correct_guess", "payload": _json(member)}


def end_round():
    return {"event": "end_round", "payload": {}}


def end_game():
    return {"event": "end_game", "payload": {}}
