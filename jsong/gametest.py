from typing import Iterable
from jsong.audio.playlist import Playlist, Track
from jsong.game import Game, GameSettings
from jsong.player import Player
import pytest


@pytest.fixture
def player():
    return Player("1", "1")


@pytest.fixture
def player2():
    return Player("2", "2")


@pytest.fixture
def correct_player():
    return Player("1", "1", 1, True)


@pytest.fixture
def members():
    return [("1", "1"), ("2", "2")]


@pytest.fixture
def playlist():
    return Playlist(
        name="K-pop",
        tracks=[
            Track(name="I don't know", artists=["Apink"], duration=0),
            Track(name="Next Level", artists=["aespa"], duration=0),
            Track(name="The Feels", artists=["TWICE"], duration=0),
        ],
    )


@pytest.fixture
def game(members: Iterable[tuple[str, str]], playlist: Playlist):
    return Game(
        members,
        Playlist(name=playlist.name, tracks=list(reversed(playlist.tracks))),
        settings=GameSettings(playlist_name=playlist.name, max_rounds=2),
    )


def test_init_game_state(
    player: Player, player2: Player, playlist: Playlist, game: Game
):
    assert game.players == {"1": player, "2": player2}
    assert game.playlist == list(reversed(playlist.tracks))
    assert game.settings == GameSettings(playlist_name=playlist.name, max_rounds=2)
    assert game.rounds == 0
    assert game.current_track is None
    assert game.is_active is True
    assert game.play_length == 20
    assert game.start_round_delay == 3


def test_guess_correct(game: Game, player: Player, playlist: Playlist):
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[0].name)
    assert game.players[player.uid].score == 1
    assert game.players[player.uid].is_correct is True
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[1].name)
    assert game.players[player.uid].score == 2
    assert game.players[player.uid].is_correct is True


def test_guess_twice_no_result(game: Game, player: Player, playlist: Playlist):
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[0].name)
    assert not game.guess(player.uid, playlist.tracks[0].name)
    assert game.players[player.uid].score == 1
    assert game.players[player.uid].is_correct is True


def test_guess_incorrect(game: Game, player: Player, playlist: Playlist):
    game.advance_round()
    assert not game.guess(player.uid, playlist.tracks[1].name)
    assert game.players[player.uid].score == 0
    assert game.players[player.uid].is_correct is False


def test_advance_round(game: Game):
    game.advance_round()
    assert game.rounds == 1
    assert len(game.playlist) == 2
    assert game.current_track is not None
    assert game.is_active is True


def test_advance_track(game: Game, playlist: Playlist):
    game.advance_track()
    assert game.current_track == playlist.tracks[0]
    game.advance_track()
    assert game.current_track == playlist.tracks[1]
    game.advance_track()
    assert game.current_track == playlist.tracks[2]
    game.advance_track()
    assert game.current_track is None


def test_next_track(game: Game, playlist: Playlist):
    assert game.next_track == playlist.tracks[0]
    game.advance_track()
    assert game.next_track == playlist.tracks[1]
    game.advance_track()
    assert game.next_track == playlist.tracks[2]
    game.advance_track()
    assert game.next_track is None


def test_is_last_round(game: Game):
    game.advance_round()
    game.advance_round()
    game.advance_round()
    assert game.is_last_round


def test_game_over_by_rounds(game: Game):
    game.advance_round()
    game.advance_round()
    game.advance_round()
    assert game.rounds == 3
    assert len(game.playlist) == 0
    assert game.current_track is not None
    assert game.is_active is False


@pytest.fixture
def game2(members: Iterable[tuple[str, str]], playlist: Playlist):
    return Game(
        members,
        playlist,
        settings=GameSettings(playlist_name=playlist.name, max_rounds=5),
    )


def test_game_over_by_playlist(game2: Game):
    for _ in range(4):
        game2.advance_round()
    assert game2.rounds == 4
    assert len(game2.playlist) == 0
    assert game2.current_track is None
    assert game2.is_active is False
