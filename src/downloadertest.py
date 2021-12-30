from playlist import Track
from downloader import DownloadedTrack, download, fileize
import pytest
from pathlib import Path


@pytest.mark.skip(reason="Takes too long")
def test_download():
    track = Track(name="Bon Bon Chocolat", artists=["EVERGLOW"])
    dtrack = download(track)
    assert isinstance(dtrack, DownloadedTrack)
    assert dtrack.track == track
    assert dtrack.extension == "webm"


def test_fileize():
    dtrack = DownloadedTrack(
        track=Track(name="Bon Bon Chocolat", artists=["EVERGLOW"]), extension="webm"
    )
    BASE_DIR = Path(__file__).resolve().parent.parent
    assert fileize(dtrack) == f"{BASE_DIR}/downloads/Bon Bon Chocolat - EVERGLOW.webm"
