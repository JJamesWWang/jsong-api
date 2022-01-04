from typing import Iterable
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
import random
from jsong.audio.playlist import Track, Playlist
from jsong.player import Player
from dataclasses import replace


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GameSettings:
    playlist_name: str
    max_rounds: int = 10
    play_length: int = 10


class Game:
    def __init__(
        self,
        members: Iterable[tuple[str, str]],
        playlist: Playlist,
        settings: GameSettings = None,
    ):
        self.players = {uid: Player(uid, username) for (uid, username) in members}
        self.playlist = playlist.tracks
        self.settings = settings or GameSettings(playlist_name=playlist.name)
        self.rounds = 0
        self.current_track: Track = None

    @classmethod
    def empty(cls):
        return cls([], Playlist.empty())

    @property
    def is_active(self):
        return self.playlist != [] and self.rounds < self.settings.max_rounds

    def guess(self, uid: str, guess: str) -> bool:
        if self._should_give_points(uid, guess):
            player = self.players[uid]
            self.players[uid] = replace(player, score=player.score + 1, is_correct=True)
            return True
        return False

    def _should_give_points(self, uid: str, guess: str):
        return (
            self.current_track.name.lower() == guess.lower()
            and self.players[uid].is_correct is False
        )

    def advance_round(self):
        if self.is_active:
            self.rounds += 1
            self.current_track = self.playlist.pop(
                random.randint(0, len(self.playlist) - 1)
            )
            self.players = {
                uid: replace(player, is_correct=False, is_ready=False)
                for uid, player in self.players.items()
            }

    def retract_round(self):
        self.rounds -= 1

    @property
    def play_length(self):
        return self.settings.play_length
