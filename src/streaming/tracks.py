"""
tracks.py
---------
Implement the class hierarchy for all playable content on the platform.

Classes to implement:
  - Track (abstract base class)
    - Song
      - SingleRelease
      - AlbumTrack
    - Podcast
      - InterviewEpisode
      - NarrativeEpisode
    - AudiobookTrack
"""
from streaming import *

from datetime import date


class Track:
    """
    Track("t1", "Track", 120, "pop")
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre

    def __eq__(self, other: Track):
        if isinstance(other, Track):
            return self.track_id == other.track_id
        else:
            return False

    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0


class Song(Track):
    """
    Song("t1", "Song", 120, "pop", Artist("a1", "Artist", genre="pop"))
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist):
        super().__init__(track_id, title, duration_seconds, genre)
        self.artist = artist


class AlbumTrack(Song):
    album: Album | None
    """
    AlbumTrack("t1", "Track", 120, "pop", artist, track_number=1)
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist, track_number: int):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None


class SingleRelease(Song):
    """
    SingleRelease("t1", "Song A", 180, "pop", artist_a, release_date=date(2024, 1, 1))
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: Artist,
                 release_date: date):
        super().__init__(track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date


class Podcast(Track):
    """
    Podcast("p1", "Pod", 1800, "podcast", host="Host")
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str = ""):
        super().__init__(track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description


class NarrativeEpisode(Podcast):
    """
    NarrativeEpisode("p1", "Ep", 1800, "podcast", host="H", season=2, episode_number=4)
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, season: int,
                 episode_number: int):
        super().__init__(track_id, title, duration_seconds, genre, host)
        self.season = season
        self.episode_number = episode_number


class InterviewEpisode(Podcast):
    """
    InterviewEpisode("p1", "Ep", 1800, "podcast", host="H", guest="G")
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, guest: str):
        super().__init__(track_id, title, duration_seconds, genre, host)
        self.guest = guest


class AudiobookTrack(Track):
    """
    AudiobookTrack("a1", "Chapter", 600, "audio", author="Auth", narrator="Narr")
    """

    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str):
        super().__init__(track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator
