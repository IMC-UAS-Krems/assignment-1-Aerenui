"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""
from streaming import *


class Artist:
    tracks: list[Track]
    """
    Artist("a1", "Artist", genre="pop")
    """
    def __init__(self, artist_id: str, name: str, genre: str):
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks = []

    def add_track(self, track: Track):
        self.tracks.append(track)

    def track_count(self) -> int:
        return len(self.tracks)
