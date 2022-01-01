import youtube_dl
from playlist import querify, Track
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DownloadedTrack:
    track: Track
    extension: str


def _generate_options(track: Track) -> dict:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    return {
        "format": "bestaudio/best",
        "noplaylist": True,
        "outtmpl": f"{BASE_DIR}/downloads/{querify(track)}.%(ext)s",
    }


def fileize(dtrack: DownloadedTrack):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    return f"{BASE_DIR}/downloads/{querify(dtrack.track)}.{dtrack.extension}"


def download(track: Track) -> DownloadedTrack:
    with youtube_dl.YoutubeDL(_generate_options(track)) as ydl:
        data = ydl.extract_info(f"ytsearch:{querify(track)}", download=True)
    return DownloadedTrack(track=track, extension=data["entries"][0]["ext"])
