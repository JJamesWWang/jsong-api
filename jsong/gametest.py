from typing import Iterable
from jsong.audio.playlist import Playlist, Track
from jsong.game import POINTS_PER_CORRECT_GUESS, Game, GameSettings
from jsong.player import Player
import pytest
import time


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
    assert game.start_round_time == 0


def test_is_round_active(game: Game):
    assert game.is_round_active is False
    game.start_round_time = time.time()
    assert game.is_round_active is True
    game.start_round_time = time.time() - game.play_length - 1
    assert game.is_round_active is False


def test_round_time_remaining(game: Game):
    game.start_round_time = time.time()
    assert game.play_length - 1 <= game.round_time_remaining <= game.play_length
    game.start_round_time = time.time() - game.play_length - 1
    assert game.round_time_remaining == 0


def test_guess_correct_title(game: Game, player: Player, playlist: Playlist):
    game.start_round_time = time.time() - game.settings.play_length + 0.05
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[0].name)
    assert (
        POINTS_PER_CORRECT_GUESS
        <= game.players[player.uid].score
        <= 2 * POINTS_PER_CORRECT_GUESS
    )
    assert game.players[player.uid].is_correct is True
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[1].name)
    assert (
        2 * POINTS_PER_CORRECT_GUESS
        <= game.players[player.uid].score
        <= 3 * POINTS_PER_CORRECT_GUESS
    )
    assert game.players[player.uid].is_correct is True


def test_guess_correct_artist(game: Game, player: Player, playlist: Playlist):
    game.start_round_time = time.time() - game.settings.play_length + 0.05
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[0].artists[0])
    assert (
        POINTS_PER_CORRECT_GUESS / 2
        <= game.players[player.uid].score
        <= POINTS_PER_CORRECT_GUESS
    )
    assert game.players[player.uid].is_correct is True


def test_matches_title(game: Game):
    # exact match
    assert game.matches_title("I don't know", "I don't know")
    # lowercase match
    assert game.matches_title("i don't know", "I don't know")
    # whitespace ignored
    assert game.matches_title("I  don't  know   ", "I don't know")
    # main title match
    assert game.matches_title("I don't know", "I don't know (?????????)")
    # alt title match
    assert game.matches_title("?????????", "I don't know (?????????)")
    # both match
    assert game.matches_title("I don't know (?????????)", "I don't know (?????????)")
    # no match
    assert not game.matches_title("I know", "I don't know")


def matches_artist(game: Game):
    # match 1
    assert game.matches_artist("Apink", ["Apink", "OH MY GIRL"])
    # match 2
    assert game.matches_artist("oh  my  girl ", ["Apink", "OH MY GIRL"])


def test_guess_twice_no_result(game: Game, player: Player, playlist: Playlist):
    game.start_round_time = time.time()
    game.advance_round()
    assert game.guess(player.uid, playlist.tracks[0].name)
    assert not game.guess(player.uid, playlist.tracks[0].name)
    assert game.players[player.uid].score >= POINTS_PER_CORRECT_GUESS
    assert game.players[player.uid].is_correct is True


def test_guess_incorrect(game: Game, player: Player, playlist: Playlist):
    game.start_round_time = time.time()
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
