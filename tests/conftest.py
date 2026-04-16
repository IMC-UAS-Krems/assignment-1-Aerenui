"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)   # well within 30-day window
OLD    = FIXED_NOW - timedelta(days=60)   # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels  = Artist("a1", "Pixels", genre="pop")
    wawes = Artist("a2", "Wawes", genre="medieval")

    platform.add_artist(pixels)
    platform.add_artist(wawes)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain",      180, "pop",  pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon",    210, "pop",  pixels, track_number=2)

    dd2 = Album("alb2", "Once upon a time", artist=wawes, release_year=1251)
    t3 = AlbumTrack("t3", "Morning sunrise",   195, "medieval",  pixels, track_number=3)

    for track in (t1, t2):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    for track in (t3,):
        dd2.add_track(track)
        platform.add_track(track)
        wawes.add_track(track)

    platform.add_album(dd)
    platform.add_album(dd2)


    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice",   age=30)
    bob   = PremiumUser("u2", "Bob",   age=25, subscription_start=date(2023, 1, 1))
    zeus = FamilyAccountUser("u3", "Zeus", age=21)
    persephone  = FamilyMember("u4", "Persephone", age=16, parent=zeus)
    zeus.add_sub_user(persephone)
    for user in (alice, bob, zeus, persephone):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Listening sessions
    # ------------------------------------------------------------------
    platform.record_session(ListeningSession("a1", alice, t1, FIXED_NOW, t1.duration_seconds))
    platform.record_session(ListeningSession("a2", alice, t2, FIXED_NOW, t2.duration_seconds))

    platform.record_session(ListeningSession("b1", bob, t1, FIXED_NOW, t1.duration_seconds))
    platform.record_session(ListeningSession("b2", bob, t2, OLD, t1.duration_seconds))
    platform.record_session(ListeningSession("b3", bob, t3, FIXED_NOW, t2.duration_seconds))

    platform.record_session(ListeningSession("z1", zeus, t1, FIXED_NOW, t1.duration_seconds-20))
    platform.record_session(ListeningSession("z2", zeus, t1, FIXED_NOW, t1.duration_seconds))

    platform.record_session(ListeningSession("p1", persephone, t2, FIXED_NOW, t2.duration_seconds-30))

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------
    pl1 = Playlist("WM", "Wierd Mix", persephone)
    pl1.add_track(t2)
    pl1.add_track(t3)
    platform.add_playlist(pl1)

    pl2 = Playlist("MN", "My only one", bob)
    pl2.add_track(t3)
    platform.add_playlist(pl2)

    pl3 = CollaborativePlaylist("KM", "Known Songs", zeus)
    pl3.add_track(t1)
    pl3.add_contributor(alice)
    platform.add_playlist(pl3)

    pl4 = CollaborativePlaylist("AS", "All known Songs", zeus)
    pl4.add_track(t1)
    pl4.add_contributor(alice)
    pl4.add_contributor(bob)
    pl4.add_contributor(persephone)
    platform.add_playlist(pl4)

    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
