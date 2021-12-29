from dataclasses import dataclass


@dataclass
class Track:
    name: str
    artists: list[str]


@dataclass
class Playlist:
    name: str
    tracks: list[Track]
