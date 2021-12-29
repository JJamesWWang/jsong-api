import pytest
import spotify


@pytest.fixture
def playlist_link() -> str:
    return (
        "https://open.spotify.com/playlist/0mAgqUtF9rEbXuIGFlIK4I?si=f0d9a82224244fde"
    )


@pytest.fixture
def access_token() -> str:
    return spotify.get_access_token()


@pytest.fixture
def playlist(playlist_link, access_token) -> spotify.Playlist:
    return spotify.get_playlist(access_token, playlist_link)


def test_get_access_token():
    assert isinstance(spotify.get_access_token(), str)


def test_get_playlist(playlist):
    assert isinstance(playlist, spotify.Playlist)


def test_playlist_name(playlist):
    assert playlist.name == "Test Playlist"


def test_playlist_tracks_exist(playlist):
    assert len(playlist.tracks) == 3


def test_playlist_tracks_correct(playlist):
    for track in playlist.tracks:
        assert track.name in ["Electric Shock", "D-D-DANCE", "GLASSY"]
        assert track.artists in [["f(x)"], ["IZ*ONE"], ["JO YURI"]]


def test_querify():
    assert (
        spotify.querify(spotify.Track(name="Electric Shock", artists=["f(x)"]))
        == "Electric Shock - f(x)"
    )
    assert (
        spotify.querify(spotify.Track(name="A", artists=["B", "C", "D"]))
        == "A - B, C, D"
    )
    assert (
        spotify.querify(spotify.Track(name="A", artists=["B C", "D E"]))
        == "A - B C, D E"
    )
