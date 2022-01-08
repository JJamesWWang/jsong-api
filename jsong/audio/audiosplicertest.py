import pytest
from playlist import Track
from downloader import download, DownloadedTrack
from audiosplicer import temp_file, splice
from pathlib import Path
import os


@pytest.fixture
def track():
    return Track(name="A", artists=["B"], duration=200000)


@pytest.fixture()
def dtrack(track: Track):
    return download(track)


def test_temp_file(dtrack: DownloadedTrack):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    assert temp_file() == f"{BASE_DIR}/downloads/temp/track.mp3"


def test_splice(dtrack: DownloadedTrack):
    splice(dtrack, start=100000, end=110000)
    assert os.path.exists(temp_file())


def test_negative_splice(dtrack: DownloadedTrack):
    with pytest.raises(ValueError):
        splice(dtrack, start=-500, end=500)


def test_backwards_splice(dtrack: DownloadedTrack):
    with pytest.raises(ValueError):
        splice(dtrack, start=5000, end=1000)


def test_splice_out_of_bounds(dtrack: DownloadedTrack):
    with pytest.raises(ValueError):
        splice(dtrack, start=500000, end=550000)
