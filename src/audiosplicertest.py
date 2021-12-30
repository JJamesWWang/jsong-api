from playlist import Track
from downloader import DownloadedTrack
from audiosplicer import temp_fileize, splice
from pathlib import Path
import os
import pytest


def test_temp_fileize():
    BASE_DIR = Path(__file__).resolve().parent.parent
    assert (
        temp_fileize(
            DownloadedTrack(track=Track(name="A", artists=["B"]), extension="mp3")
        )
        == f"{BASE_DIR}/downloads/temp/A - B.mp3"
    )


# @pytest.mark.skip("Dependends on downloader")
def test_splice():
    BASE_DIR = Path(__file__).resolve().parent.parent
    dtrack = DownloadedTrack(
        track=Track(name="Bon Bon Chocolat", artists=["EVERGLOW"]), extension="webm"
    )
    splice(dtrack, start=100000, end=110000)
    assert os.path.exists(temp_fileize(dtrack))
