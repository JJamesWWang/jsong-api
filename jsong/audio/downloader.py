import youtube_dl
from jsong.audio.playlist import querify, encode, Track
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
        "outtmpl": f"{BASE_DIR}/downloads/{encode(track)}.%(ext)s",
        "cookiefile": f"{BASE_DIR}/cookies.txt",
        "external_downloader": "aria2c",
        "external_downloader_args": ["-s 16", "-x 16", "-k 1M"],
    }


def fileize(dtrack: DownloadedTrack):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    return f"{BASE_DIR}/downloads/{encode(dtrack.track)}.{dtrack.extension}"


def download(track: Track) -> DownloadedTrack:
    with youtube_dl.YoutubeDL(_generate_options(track)) as ydl:
        data = ydl.extract_info(f"ytsearch:{querify(track)}", download=True)
    return DownloadedTrack(track=track, extension=data["entries"][0]["ext"])
