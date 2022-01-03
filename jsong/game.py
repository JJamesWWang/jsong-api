from typing import Iterable
from dataclasses import dataclass
from pydantic import BaseModel
import random

from jsong.audio.playlist import Track, Playlist


@dataclass
class Player:
    uid: str
    score: int = 0
    is_correct: bool = False

    @classmethod
    def with_correct(cls, player):
        return cls(player.uid, player.score + 1, True)

    @classmethod
    def with_advance_round(cls, player):
        return cls(player.uid, player.score, False)


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

    def guess(self, uid: str, guess: str):
        if self._should_give_points(uid, guess):
            self.players[uid] = Player.with_correct(self.players[uid])

    def _should_give_points(self, uid: str, guess: str):
        print(self.current_track.name, guess)
        return (
            self.current_track.name.lower() == guess.lower()
            and self.players[uid].is_correct is False
        )

    def advance_round(self):
        if not self.is_over:
            self.rounds += 1
            self.current_track = self.playlist.pop(
                random.randint(0, len(self.playlist) - 1)
            )
            self.players = {
                uid: Player.with_advance_round(player)
                for uid, player in self.players.items()
            }
