from playlist import Track
from downloader import DownloadedTrack, download, fileize
import pytest


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
    assert fileize(dtrack) == "Bon Bon Chocolat - EVERGLOW.webm"
