import pytest
from playlist import encode, Track
from downloader import DownloadedTrack, download, fileize
from pathlib import Path
import os


@pytest.fixture
def track():
    return Track(name="Bon Bon Chocolat", artists=["EVERGLOW"], duration=0)


def test_download(track: Track):
    dtrack = download(track)
    assert isinstance(dtrack, DownloadedTrack)
    assert dtrack.track == track
    assert dtrack.extension == "webm"
    assert os.path.exists(fileize(dtrack))


def test_fileize(track: Track):
    dtrack = DownloadedTrack(track=track, extension="webm")
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    encoded = encode(track)
    assert fileize(dtrack) == f"{BASE_DIR}/downloads/{encoded}.webm"
