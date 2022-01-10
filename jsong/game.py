from typing import Iterable
from dataclasses import dataclass, replace
from dataclasses_json import dataclass_json, LetterCase
import time
from jsong.audio.playlist import Track, Playlist
from jsong.player import Player


POINTS_PER_CORRECT_GUESS = 100


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GameSettings:
    playlist_name: str
    max_rounds: int = 10
    play_length: int = 20
    start_round_delay: int = 3


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
        self.start_round_time = 0

    @classmethod
    def empty(cls):
        return cls([], Playlist.empty())

    @property
    def is_active(self):
        return (
            self.playlist != [] or self.current_track is not None
        ) and self.rounds <= self.settings.max_rounds

    @property
    def round_time_remaining(self):
        return max(0, self.settings.play_length - (time.time() - self.start_round_time))

    @property
    def is_round_active(self):
        return self.round_time_remaining > 0

    def guess(self, uid: str, guess: str) -> bool:
        if self._should_give_points(uid, guess):
            player = self.players[uid]
            self.players[uid] = replace(
                player,
                score=self.calculate_new_score(guess, player.score),
                is_correct=True,
            )
            return True
        return False

    def _should_give_points(self, uid: str, guess: str):
        return (
            self.is_round_active
            and self.players[uid].is_correct is False
            and (
                self.matches_title(guess, self.current_track.name)
                or self.matches_artist(guess, self.current_track.artists)
            )
        )

    def matches_title(self, guess: str, title: str):
        guess, title = self.normalize(guess), self.normalize(title)
        if guess == title:
            return True
        left_parenthesis, right_parenthesis = title.find("("), title.rfind(")")
        if left_parenthesis != -1 and right_parenthesis != -1:
            main_title = self.normalize(title[:left_parenthesis])
            alt_title = self.normalize(title[left_parenthesis + 1 : right_parenthesis])
            return guess in [main_title, alt_title]
        return False

    def normalize(self, string: str):
        return " ".join(string.lower().strip().split())

    def matches_artist(self, guess: str, artists: list):
        guess, artists = self.normalize(guess), [
            self.normalize(artist) for artist in artists
        ]
        if guess in artists:
            return True

    # exponential decay to reward faster guesses
    def calculate_new_score(self, guess: str, score: int):
        points_awarded = round(
            pow(20, self.round_time_remaining / self.settings.play_length)
            * POINTS_PER_CORRECT_GUESS
        )
        if self.matches_artist(guess, self.current_track.artists):
            points_awarded //= 2
        return score + points_awarded

    def advance_round(self):
        if self.is_active:
            self.rounds += 1
            self.current_track = self.playlist.pop() if self.playlist else None
            self.players = {
                uid: replace(player, is_correct=False, is_ready=False)
                for uid, player in self.players.items()
            }

    def advance_track(self):
        self.current_track = self.playlist.pop() if self.playlist else None

    @property
    def play_length(self):
        return self.settings.play_length

    @property
    def start_round_delay(self):
        return self.settings.start_round_delay

    @property
    def next_track(self):
        return self.playlist[-1] if self.playlist else None

    @property
    def is_last_round(self):
        return self.rounds == self.settings.max_rounds or self.playlist == []
