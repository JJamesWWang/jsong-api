from typing import Iterable
from dataclasses import dataclass
from pydantic import BaseModel
import random

from jsong.audio.playlist import Track, Playlist


@dataclass
class Player:
    uid: str
    score: int = 0
    guessed_correctly: bool = False


class GameSettings(BaseModel):
    playlistName: str
    maxRounds: int = 10


class Game:
    def __init__(
        self, uids: Iterable[str], playlist: Playlist, settings: GameSettings = None
    ):
        self.players = {uid: Player(uid) for uid in uids}
        self.playlist = playlist.tracks
        self.settings = settings or GameSettings(playlistName=playlist.name)
        self.rounds = 0
        self.current_track: Track = None

    @property
    def is_over(self):
        return self.playlist == [] or self.rounds >= self.settings.maxRounds

    def advance_round(self):
        if not self.is_over:
            self.rounds += 1
            self.current_track = self.playlist.pop(
                random.randint(0, len(self.playlist) - 1)
            )
