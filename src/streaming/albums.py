"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from streaming import *


class Album:
    tracks: list[AlbumTrack]
    """
    Album("alb1", "Album", artist=artist, release_year=2024)
    """
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track: AlbumTrack):
        self.tracks.append(track)
        self.tracks.sort(key=lambda a: a.track_id, reverse=True)
        track.album = self

    def track_ids(self) -> set[str]:
        return set(t.track_id for t in self.tracks)

    def duration_seconds(self) -> int:
        return sum([t.duration_seconds for t in self.tracks])

