import requests
from decouple import config
import base64
from jsong.audio.playlist import Playlist, Track


def _get_access_token() -> str:
    return requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        headers={
            "Authorization": "Basic "
            + base64.b64encode(
                bytes(
                    f"{config('SPOTIFY_CLIENT_ID')}:{config('SPOTIFY_CLIENT_SECRET')}",
                    "utf-8",
                )
            ).decode("utf-8"),
            "Content-Type": "application/x-www-form-urlencoded",
        },
    ).json()["access_token"]


def get_playlist(playlist_link: str) -> Playlist:
    playlist_id = playlist_link.split("/")[-1]
    playlist_data = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}",
        headers={"Authorization": f"Bearer {_get_access_token()}"},
    ).json()

    tracks = []
    for track in playlist_data["tracks"]["items"]:
        try:
            tracks.append(
                Track(
                    name=track["track"]["name"],
                    artists=[artist["name"] for artist in track["track"]["artists"]],
                    duration=track["track"]["duration_ms"],
                )
            )
        except KeyError:
            pass    # invalid track okay, just skip it
    return Playlist(name=playlist_data["name"], tracks=tracks)
