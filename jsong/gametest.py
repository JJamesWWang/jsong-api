from typing import Iterable
from jsong.audio.playlist import Playlist, Track
from jsong.game import Game, GameSettings, Player
import pytest

from jsong.member import Member


@pytest.fixture
def uids():
    return ["1", "2"]


@pytest.fixture
def playlist():
    return Playlist(
        name="K-pop",
        tracks=[
            Track(name="I don't know", artists=["Apink"]),
            Track(name="Next Level", artists=["aespa"]),
            Track(name="The Feels", artists=["TWICE"]),
        ],
    )


@pytest.fixture
def game1(uids: Iterable[str], playlist: Playlist):
    return Game(
        uids, playlist, settings=GameSettings(playlistName=playlist.name, maxRounds=2)
    )


def test_init_game_state(playlist: Playlist, game1: Game):
    assert game1.players == {"1": Player("1"), "2": Player("2")}
    assert game1.playlist == playlist.tracks
    assert game1.settings == GameSettings(playlistName=playlist.name, maxRounds=2)
    assert game1.rounds == 0
    assert game1.current_track is None
    assert game1.is_over is False


def test_advance_round(game1: Game):
    game1.advance_round()
    assert game1.rounds == 1
    assert len(game1.playlist) == 2
    assert game1.current_track is not None
    assert game1.is_over is False


def test_game_over_by_rounds(game1: Game):
    game1.advance_round()
    game1.advance_round()
    assert game1.rounds == 2
    assert len(game1.playlist) == 1
    assert game1.current_track is not None
    assert game1.is_over is True


@pytest.fixture
def game2(uids: Iterable[str], playlist: Playlist):
    return Game(
        uids, playlist, settings=GameSettings(playlistName=playlist.name, maxRounds=5)
    )


def test_game_over_by_playlist(game2: Game):
    for _ in range(3):
        game2.advance_round()
    assert game2.rounds == 3
    assert len(game2.playlist) == 0
    assert game2.current_track is not None
    assert game2.is_over is True
