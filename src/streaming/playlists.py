"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
from streaming import *


class Playlist:
    tracks: list[Track]
    """
    playlist = Playlist("p1", "Mix", owner=User("u1", "Owner", age=25))
    """
    def __init__(self, playlist_id: str, name: str, owner: User):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track: Track):
        if len([t for t in self.tracks if t.track_id == track.track_id]) == 0:
            self.tracks.append(track)

    def remove_track(self, track_id: str):
        self.tracks = [t for t in self.tracks if t.track_id != track_id]

    def total_duration_seconds(self) -> int:
        return sum([t.duration_seconds for t in self.tracks])

class CollaborativePlaylist(Playlist):
    contributors: list[User]

    def __init__(self, playlist_id: str, name: str, owner: User):
        super().__init__(playlist_id, name, owner)
        self.contributors = [owner]

    def add_contributor(self, user: User):
        if len([u for u in self.contributors if u.user_id == user.user_id]) == 0:
            self.contributors.append(user)

    def remove_contributor(self, user: User):
        if user.user_id != self.owner.user_id:
            self.contributors.remove(user)