from pydub import AudioSegment
from pathlib import Path
import os
from jsong.audio.downloader import fileize, DownloadedTrack


def temp_file():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    return f"{BASE_DIR}/downloads/temp/track.mp3"


def splice(dtrack: DownloadedTrack, start: int, end: int) -> None:
    duration = dtrack.track.duration
    if start < 0 or end < 0 or start > duration or end > duration or start > end:
        raise ValueError
    audio = AudioSegment.from_file(fileize(dtrack), dtrack.extension)
    os.makedirs(os.path.dirname(temp_file()), exist_ok=True)
    with open(temp_file(), "wb") as f:
        audio[start:end].export(f, format="mp3")
