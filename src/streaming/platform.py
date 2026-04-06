"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import UTC, timedelta
from datetime import datetime
from streaming import *
from streaming.users import *


class StreamingPlatform:
    name: str
    _catalogue: dict[str, Track]
    _users: dict[str, User]
    _artists: dict[str, Artist]
    _albums: dict[str, Album]
    _playlists: dict[str, Playlist]
    _sessions: list[ListeningSession]
    """
    StreamingPlatform("TestStream")
    """

    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track):
        self._catalogue[track.track_id] = track

    def add_user(self, user):
        self._users[user.user_id] = user

    def add_artist(self, artist):
        self._artists[artist.artist_id] = artist

    def add_album(self, album):
        self._albums[album.album_id] = album

    def add_playlist(self, playlist):
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self._sessions.append(session)
        self._users.get(session.user.user_id).add_session(session)

    def get_track(self, track_id) -> Track | None:
        return self._catalogue.get(track_id)

    def get_user(self, user_id) -> User | None:
        return self._users.get(user_id)

    def get_artist(self, artist_id) -> Artist | None:
        self._artists.get(artist_id)

    def get_album(self, album_id) -> Album | None:
        self._albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())

    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        """
        Return the total cumulative listening time (in minutes) across all users for a given time period. Sum up the listening duration for all sessions that fall within the specified datetime window (inclusive on both ends).
        """
        #start_time, end_time = start.now(UTC), end.now(UTC)
        # assert [[s.duration_listened_seconds for s in u.sessions if start_time <= s.timestamp.now(UTC) <= end_time]
        #      for u in self._users.values()] == 1
        return sum(
            [sum([s.duration_listened_seconds for s in u.sessions if start <= s.timestamp <= end])
             for u in self._users.values()]) / 60.0

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        """
        Compute the average number of unique tracks listened to per PremiumUser in the last days days (default 30). Only count distinct tracks for sessions within the time window. Return 0.0 if there are no premium users.
        """
        premiums = [u for u in self._users.values() if isinstance(u, PremiumUser)]
        if len(premiums) == 0:
            return 0.0

        d_limit = datetime.now() - timedelta(days)

        cnt = 0
        for u in premiums:
            cnt += len(set([s.track.track_id for s in u.sessions if s.timestamp >= d_limit]))

        return cnt / len(premiums)

    def track_with_most_distinct_listeners(self) -> Track | None:
        """
        Return the track with the highest number of distinct listeners (not total plays) in the catalogue. Count the number of unique users who have listened to each track and return the one with the most. Return None if no sessions exist.
        """
        counter = {}
        for s in self._sessions:
            if not s.track.track_id in counter.keys():
                counter[s.track.track_id] = 1
            else:
                counter[s.track.track_id] += 1
        tracks = list(counter.items())
        tracks.sort(key=lambda a: a[0])
        if len(tracks) == 0:
            return None

        return self._catalogue.get(tracks[0][0])

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        """
        For each user subtype (e.g., FreeUser, PremiumUser, FamilyAccountUser, FamilyMember), compute the average session duration (in seconds) and return them ranked from longest to shortest. Return as a list of (type_name, average_duration_seconds) tuples.
        """
        classes = [
            (FreeUser, "FreeUser"),
            (PremiumUser, "PremiumUser"),
            (FamilyAccountUser, "FamilyAccountUser"),
            (FamilyMember, "FamilyMember")
        ]
        times = {c[1]: {"time": 0, "cnt": 0} for c in classes}
        for user in list(self._users.values()):
            selector = [n for (c, n) in classes if isinstance(user, c)][0]
            d = 0 if len(user.sessions) == 0 else sum([s.duration_listened_seconds for s in user.sessions]) / len(
                user.sessions)
            times[selector]["time"] += d
            times[selector]["cnt"] += 1
        ot = [(a, b["time"] / b["cnt"] if b["cnt"] != 0 else 0.0) for (a, b) in times.items()]
        ot.sort(key=lambda a: a[1], reverse=True)
        return ot

    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        """
        Return the total listening time (in minutes) attributed to tracks associated with FamilyAccountUser sub-accounts where the sub-account holder (i.e., FamilyMember) is under the specified age threshold (default 18, exclusive). For example, with threshold 18, count only family members with age < 18.
        """
        families = [u for u in self._users.values() if isinstance(u, FamilyAccountUser)]
        time = 0.0
        for f in families:
            time += sum([u.total_listening_minutes() for u in f.sub_users if u.age < age_threshold])
        return time

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        """
        Identify the top n artists (default 5) ranked by total cumulative listening time across all their tracks. Only count listening time for tracks where isinstance(track, Song) is true (exclude podcasts and audiobooks). Return as a list of (Artist, total_minutes) tuples, sorted from highest to lowest listening time.
        """
        # [[track. for track in a.tracks if isinstance(track, Song)] for a in self._artists.values()]
        minutes = {a.artist_id: [0.0, a] for a in self._artists.values()}
        for user in self._users.values():
            for session in user.sessions:
                if isinstance(session.track, Song):
                    minutes.get(session.track.artist.artist_id)[0] += session.duration_listened_minutes()

        return [(item[1], item[0]) for item in minutes.values()][:min(5, len(minutes))]

    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        """
        Given a user ID, return their most frequently listened-to genre and the percentage of their total listening time it accounts for. Return a (genre, percentage) tuple where percentage is in the range [0, 100], or None if the user doesn't exist or has no listening history.
        """
        user = self._users.get(user_id)
        if user is None:
            return None

        counter = {}
        if len(user.sessions) == 0:
            return None

        for s in user.sessions:
            if s.track.genre in counter.keys():
                counter[s.track.genre] += 1
            else:
                counter[s.track.genre] = 1

        return sorted(counter.items(), key=lambda a: a[1])[0]

    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        """
        Return all CollaborativePlaylist instances that contain tracks from more than threshold (default 3) distinct artists. Only Song tracks count toward the artist count (exclude Podcast and AudiobookTrack which don't have artists). Return playlists in the order they were registered.
        """
        colabs: list[CollaborativePlaylist] = [playlist for playlist in self._playlists.values() if
                                               isinstance(CollaborativePlaylist, playlist)]
        result = []
        for colab in colabs:
            if len(colab.contributors) <= threshold:
                continue
            if len([1 for track in colab.tracks if not isinstance(Song, track)]) > 0:
                continue
            result.append(colab)
        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        """
        Compute the average number of tracks per playlist, distinguishing between standard Playlist and CollaborativePlaylist instances. Return a dictionary with keys "Playlist" and "CollaborativePlaylist" mapped to their respective averages. Return 0.0 for a type with no instances.
        """
        result = {
            "Playlist": {
                "val": 0.0,
                "cnt": 0
            },
            "CollaborativePlaylist": {
                "val": 0.0,
                "cnt": 0
            }
        }
        for playlist in self._playlists.values():
            key = "Playlist"
            if isinstance(CollaborativePlaylist, playlist):
                key = "CollaborativePlaylist"
            result[key]["val"] += len(playlist.tracks)
            result[key]["cnt"] += 1

        return {k: 0.0 if v["cnt"] == 0 else v["val"] / v["cnt"] for k, v in result.items()}

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        """
        Identify users who have listened to every track on at least one complete Album and return the corresponding album titles. A user "completes" an album if their session history includes at least one listen to each track on that album. Return as a list of (User, [album_title, ...]) tuples in registration order. Albums with no tracks are ignored.
        """
        listened_full_ids_per_user: dict[User, list[str]] = {
            user: [s.track.track_id for s in user.sessions if s.duration_listened_seconds == s.track.duration_seconds]
            for user in self._users.values()
        }
        track_ids_per_album: dict[Album, list[str]] = {
            album:
                [at.track_id for at in album.tracks]
            for album in self._albums.values() if len(album.tracks) != 0
        }

        output = []
        for (user, listened_full) in listened_full_ids_per_user.items():
            if len(listened_full) == 0:
                continue
            copy_listened = list(listened_full)
            albums = set()
            while len(copy_listened) > 0:
                n = copy_listened.pop()
                album = [k for k, v in track_ids_per_album.items() if n in v][0]
                albums.add(album.title)
            output.append((user, list(albums)))
        return output
