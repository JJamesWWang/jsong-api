from dataclasses import dataclass
from dataclasses_json import dataclass_json
import base64


@dataclass_json
@dataclass
class Track:
    name: str
    artists: list[str]
    duration: int


@dataclass
class Playlist:
    name: str
    tracks: list[Track]

    @classmethod
    def empty(cls):
        return cls("", [])


def querify(track: Track) -> str:
    return f"{track.name} - {', '.join(track.artists)}"


def encode(track: Track) -> bytes:
    return base64.urlsafe_b64encode(
        bytes(f"{track.name}-{'-'.join(track.artists)}", "utf-8")
    )
