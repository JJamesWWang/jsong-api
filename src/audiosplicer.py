from downloader import fileize, DownloadedTrack
from pydub import AudioSegment
from pathlib import Path
from playlist import querify
import os


def temp_fileize(dtrack: DownloadedTrack):
    BASE_DIR = Path(__file__).resolve().parent.parent
    return f"{BASE_DIR}/downloads/temp/{querify(dtrack.track)}.{dtrack.extension}"


def splice(dtrack: DownloadedTrack, start: int, end: int) -> None:
    audio = AudioSegment.from_file(fileize(dtrack), dtrack.extension)
    temp_filename = temp_fileize(dtrack)
    os.makedirs(os.path.dirname(temp_filename), exist_ok=True)
    with open(temp_filename, "wb") as f:
        audio[start:end].export(f, format=dtrack.extension)
