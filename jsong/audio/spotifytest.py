import pytest
import spotify
from playlist import Playlist


@pytest.fixture
def playlist_link() -> str:
    return (
        "https://open.spotify.com/playlist/0mAgqUtF9rEbXuIGFlIK4I?si=f0d9a82224244fde"
    )


@pytest.fixture
def playlist(playlist_link) -> Playlist:
    return spotify.get_playlist(playlist_link)


def test_playlist_name(playlist):
    assert playlist.name == "Test Playlist"


def test_playlist_tracks_exist(playlist):
    assert len(playlist.tracks) == 3


def test_playlist_tracks_correct(playlist):
    for track in playlist.tracks:
        assert track.name in ["Electric Shock", "D-D-DANCE", "GLASSY"]
        assert track.artists in [["f(x)"], ["IZ*ONE"], ["JO YURI"]]
        assert track.duration in [196946, 205066, 189933]

