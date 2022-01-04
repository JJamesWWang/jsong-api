from jsong.member import Member
from jsong.player import Player
from jsong.game import Game


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


def start_game(game: Game):
    return {
        "event": "start_game",
        "payload": {
            "players": list(map(lambda p: p.asdict(), game.players.values())),
            "settings": game.settings.asdict(),
        },
    }


def next_round():
    return {"event": "next_round", "payload": {}}


def start_round():
    return {"event": "start_round", "payload": {}}


def correct_guess(player: Player):
    return {"event": "correct_guess", "payload": player.asdict()}


def end_round(game: Game):
    return {"event": "end_round", "payload": game.current_track.asdict()}


def end_game():
    return {"event": "end_game", "payload": {}}
