import pytest
from datetime import date

from streaming import *

@pytest.fixture
def artist_a() -> Artist:
    return Artist("a1", "Artist A", genre="pop")


@pytest.fixture
def artist_b() -> Artist:
    return Artist("a2", "Artist B", genre="rock")


@pytest.fixture
def free_user() -> FreeUser:
    return FreeUser("u1", "User A", age=30)


@pytest.fixture
def premium_user() -> PremiumUser:
    return PremiumUser("u2", "User B", age=28, subscription_start=date(2023, 1, 1))


@pytest.fixture
def family_user() -> FamilyAccountUser:
    return FamilyAccountUser("u3", "Parent", age=40)


@pytest.fixture
def family_member(family_user: FamilyAccountUser) -> FamilyMember:
    return FamilyMember("u4", "Child", age=16, parent=family_user)


@pytest.fixture
def single_release(artist_a: Artist) -> SingleRelease:
    return SingleRelease("t1", "Song A", 180, "pop", artist_a, release_date=date(2024, 1, 1))


@pytest.fixture
def another_release(artist_b: Artist) -> SingleRelease:
    return SingleRelease("t2", "Song B", 200, "rock", artist_b, release_date=date(2024, 1, 2))


@pytest.fixture
def album_track1(artist_a: Artist) -> AlbumTrack:
    return AlbumTrack("t3", "Album Track 1", 140, "pop", artist_a, track_number=2)


@pytest.fixture
def album_track2(artist_a: Artist) -> AlbumTrack:
    return AlbumTrack("t4", "Album Track 2", 160, "pop", artist_a, track_number=1)


@pytest.fixture
def album(artist_a: Artist) -> Album:
    return Album("alb1", "Album A", artist=artist_a, release_year=2024)
