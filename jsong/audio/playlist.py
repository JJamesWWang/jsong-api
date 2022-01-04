from dataclasses import dataclass


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
