import youtube_dl
from playlist import querify, Track
from dataclasses import dataclass


@dataclass
class DownloadedTrack:
    track: Track
    extension: str


def _generate_options(track: Track) -> dict:
    return {
        "format": "bestaudio/best",
        "noplaylist": True,
        "outtmpl": f"../downloads/{querify(track)}.%(ext)s",
    }


def fileize(dtrack: DownloadedTrack):
    return f"{querify(dtrack.track)}.{dtrack.extension}"


def download(track: Track) -> DownloadedTrack:
    with youtube_dl.YoutubeDL(_generate_options(track)) as ydl:
        data = ydl.extract_info(f"ytsearch:{querify(track)}", download=True)
    return DownloadedTrack(track=track, extension=data["entries"][0]["ext"])
