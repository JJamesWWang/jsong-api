from typing import Iterable
from jsong.audio.playlist import Playlist, Track
from jsong.game import Game, GameSettings, Player
import pytest
import random
import copy


@pytest.fixture
def player():
    return Player("1")


@pytest.fixture
def correct_player():
    return Player("1", 1, True)


def test_player_with_correct(player: Player):
    player = Player.with_correct(player)
    assert player.uid == "1"
    assert player.score == 1
    assert player.is_correct is True


def test_player_with_advance_round_correct(correct_player: Player):
    player = Player.with_advance_round(correct_player)
    assert player.uid == "1"
    assert player.score == 1
    assert player.is_correct is False


def test_player_with_advance_round_incorrect(player: Player):
    player = Player("1")
    player = Player.with_advance_round(player)
    assert player.uid == "1"
    assert player.score == 0
    assert player.is_correct is False


########################################################################################


@pytest.fixture
def uids():
    return ["1", "2"]


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
def game(uids: Iterable[str], playlist: Playlist):
    random.seed(1)  # picks the first one all three times
    return Game(
        uids,
        copy.deepcopy(playlist),
        settings=GameSettings(playlistName=playlist.name, maxRounds=2),
    )


def test_init_game_state(playlist: Playlist, game: Game):
    assert game.players == {"1": Player("1"), "2": Player("2")}
    assert game.playlist == playlist.tracks
    assert game.settings == GameSettings(playlistName=playlist.name, maxRounds=2)
    assert game.rounds == 0
    assert game.current_track is None
    assert game.is_active is True


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


def test_game_over_by_rounds(game: Game):
    game.advance_round()
    game.advance_round()
    assert game.rounds == 2
    assert len(game.playlist) == 1
    assert game.current_track is not None
    assert game.is_active is False


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
    assert game2.is_active is False
