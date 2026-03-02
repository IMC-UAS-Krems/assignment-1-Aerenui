[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Fv7mIedl)
# Music Streaming Platform - Programming II Assignment

A Python 3.10+ object-oriented programming exercise. Your task is to implement the streaming platform domain model based on the specifications below.

---

## 🎯 Your Assignment

You have been hired by a major music industry corporation to build the prototype of a **music streaming platform**. This platform will serve as the foundation for managing a vast ecosystem of artists, albums, tracks, and millions of listening sessions.

### Business Requirements

Your platform must:
- **Manage content**: Artists, albums (with track ordering), individual tracks (songs, podcasts, audiobooks), and their metadata
- **Handle users**: Support different user tiers (free, premium) and family sharing accounts with sub-users
- **Track activity**: Record when users listen to tracks, including duration and timestamp
- **Organize content**: Allow users to create personalized and collaborative playlists
- **Analyze behavior**: Provide powerful analytics to understand user engagement, discover trending artists, and optimize the platform

### Your Challenge

Implement a robust **domain model** (18 classes) that captures all these requirements. Your implementation will be tested against a comprehensive test suite simulating real-world usage patterns. You must also implement **10 analytical query methods** that provide business intelligence on user listening behavior, artist popularity, album completion rates, and more.

---

## 📁 Project Structure & Class Diagram

![StreamingPlatform Class Diagram](StreamingPlatform.png)

The diagram above visualizes the complete domain model with all classes, their relationships, and the package organization.

---

## 🔍 Query Methods to Implement in StreamingPlatform

Your goal is to implement the `StreamingPlatform` class with methods that allow you to perform complex queries on the platform data. These methods will be used to analyze user behavior, track popularity, and gain insights into how the platform is being used.

These methods perform analytical queries on the platform data. Implement each of the following 10 methods in the `StreamingPlatform` class:

### Q1: Total Cumulative Listening Time
**Method:** `total_listening_time_minutes(start: datetime, end: datetime) -> float`

Return the total cumulative listening time (in minutes) across all users for a given time period. Sum up the listening duration for all sessions that fall within the specified datetime window (inclusive on both ends).

---

### Q2: Average Unique Tracks per Premium User
**Method:** `avg_unique_tracks_per_premium_user(days: int = 30) -> float`

Compute the average number of unique tracks listened to per `PremiumUser` in the last `days` days (default 30). Only count distinct tracks for sessions within the time window. Return 0.0 if there are no premium users.

---

### Q3: Track with Most Distinct Listeners
**Method:** `track_with_most_distinct_listeners() -> Track | None`

Return the track with the highest number of distinct listeners (not total plays) in the catalogue. Count the number of unique users who have listened to each track and return the one with the most. Return `None` if no sessions exist.

---

### Q4: Average Session Duration by User Type
**Method:** `avg_session_duration_by_user_type() -> list[tuple[str, float]]`

For each user subtype (e.g., `FreeUser`, `PremiumUser`, `FamilyAccountUser`, `FamilyMember`), compute the average session duration (in seconds) and return them ranked from longest to shortest. Return as a list of `(type_name, average_duration_seconds)` tuples.

---

### Q5: Total Listening Time for Underage Sub-Users
**Method:** `total_listening_time_underage_sub_users_minutes(age_threshold: int = 18) -> float`

Return the total listening time (in minutes) attributed to tracks associated with `FamilyAccountUser` sub-accounts where the sub-account holder (i.e., `FamilyMember`) is under the specified age threshold (default 18, exclusive). For example, with threshold 18, count only family members with age < 18.

---

### Q6: Top Artists by Listening Time
**Method:** `top_artists_by_listening_time(n: int = 5) -> list[tuple[Artist, float]]`

Identify the top `n` artists (default 5) ranked by total cumulative listening time across all their tracks. Only count listening time for tracks where `isinstance(track, Song)` is true (exclude podcasts and audiobooks). Return as a list of `(Artist, total_minutes)` tuples, sorted from highest to lowest listening time.

---

### Q7: User's Top Genre
**Method:** `user_top_genre(user_id: str) -> tuple[str, float] | None`

Given a user ID, return their most frequently listened-to genre and the percentage of their total listening time it accounts for. Return a `(genre, percentage)` tuple where percentage is in the range [0, 100], or `None` if the user doesn't exist or has no listening history.

---

### Q8: Collaborative Playlists with Many Artists
**Method:** `collaborative_playlists_with_many_artists(threshold: int = 3) -> list[CollaborativePlaylist]`

Return all `CollaborativePlaylist` instances that contain tracks from more than `threshold` (default 3) distinct artists. Only `Song` tracks count toward the artist count (exclude `Podcast` and `AudiobookTrack` which don't have artists). Return playlists in the order they were registered.

---

### Q9: Average Tracks per Playlist Type
**Method:** `avg_tracks_per_playlist_type() -> dict[str, float]`

Compute the average number of tracks per playlist, distinguishing between standard `Playlist` and `CollaborativePlaylist` instances. Return a dictionary with keys `"Playlist"` and `"CollaborativePlaylist"` mapped to their respective averages. Return 0.0 for a type with no instances.

---

### Q10: Users Who Completed Albums
**Method:** `users_who_completed_albums() -> list[tuple[User, list[str]]]`

Identify users who have listened to every track on at least one complete `Album` and return the corresponding album titles. A user "completes" an album if their session history includes at least one listen to each track on that album. Return as a list of `(User, [album_title, ...])` tuples in registration order. Albums with no tracks are ignored.

---


## 🚀 Setup Instructions

### 1️⃣ Clone or Extract the Repository

```bash
cd music_streaming_platform
```

### 2️⃣ Create a Python Virtual Environment

A virtual environment isolates your project dependencies. You should do this before running any code.

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On Windows (Command Prompt):
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Verify your venv is active** - you should see `(venv)` in your terminal prompt.

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install pytest
pip install -e .
```

---

## ✅ Running Tests

### Run All Tests
```bash
pytest
```

### Run All Unit Tests
```bash
pytest tests/unit_tests/ -v
```

### Run a Specific Test File
```bash
# Test only the Track classes
pytest tests/unit_tests/test_tracks.py -v

# Test only the Platform class
pytest tests/unit_tests/test_platform_registry.py -v
pytest tests/unit_tests/test_platform_sessions.py -v
```

### Run Tests with Output
```bash
# Show print statements and detailed output
pytest -v -s
```

### Run Tests and Stop on First Failure
```bash
pytest -x
```

---

## 📋 Implementation Checklist

Each file in `src/streaming/` contains a docstring specifying which classes must be implemented.

### tracks.py
- [X] `Track` - Abstract base class for all playable content
- [X] `Song` - Music track associated with an artist
- [X] `SingleRelease` - Song released as standalone single
- [X] `AlbumTrack` - Song that is part of an album
- [X] `Podcast` - Podcast episode
- [X] `InterviewEpisode` - Interview-format podcast
- [X] `NarrativeEpisode` - Narrative-format podcast
- [X] `AudiobookTrack` - Chapter/section from an audiobook

### users.py
- [X] `User` - Base class for all users
- [X] `FreeUser` - Free tier user with limited features
- [X] `PremiumUser` - Paid subscriber with full access
- [X] `FamilyAccountUser` - Premium user managing family account
- [X] `FamilyMember` - User profile belonging to a family account

### artists.py
- [X] `Artist` - Music artist or content creator

### albums.py
- [X] `Album` - Ordered collection of AlbumTrack objects

### playlists.py
- [X] `Playlist` - User-curated ordered collection of tracks
- [X] `CollaborativePlaylist` - Playlist with multiple contributors

### sessions.py
- [X] `ListeningSession` - Records a user listening to a track

### platform.py
- [X] `StreamingPlatform` - Central platform orchestrating all entities
  - Registration methods: `add_track()`, `add_user()`, `add_artist()`, `add_album()`, `add_playlist()`, `record_session()`
  - Accessors: `get_track()`, `get_user()`, `get_artist()`, `get_album()`, `all_users()`, `all_tracks()`
  - **10 Query Methods** (Q1-Q10) - See section below

# todo

- [ ] write more tests as required

## 📚 Hints & Tips

1. **Read the test files first** - They show you exactly what's expected
2. **Look at `conftest.py`** - It contains example data and shows how the classes should be used
3. **Implement classes in order** - Start with base classes before subclasses:
   - First: `Track`, `User`, `Artist`, `Album`, `Playlist`, `ListeningSession`
   - Then: Subclasses of the above
   - Finally: `StreamingPlatform` with all its methods
4. **Use type hints** - The provided docstrings include parameter and return type hints
5. **Test frequently** - Run `pytest` after implementing each class
6. **Check inheritance** - Make sure subclasses properly call `super().__init__()`

---

## 🔄 Continuous Integration

Every push to this repository automatically runs all tests via GitHub Actions.
Check the **Actions** tab to see if your implementation passes.

---

## 📖 Additional Resources

- **Python docs**: https://docs.python.org/3/
- **pytest docs**: https://docs.pytest.org/
- **Type hints**: https://docs.python.org/3/library/typing.html

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'streaming'"
Make sure you have:
1. ✅ Created and activated your virtual environment
2. ✅ Installed the package: `pip install -e .`
3. ✅ Are in the correct directory: `cd music_streaming_platform`

### Tests import but don't run
Run with verbose output to see errors:
```bash
pytest -v
```

### "pytest not found"
Install it:
```bash
pip install pytest
```

---

## 📞 Need Help?

- Check the test files for expected behavior
- Read the docstrings in skeleton files
- Ask your instructor or classmates
- Review the provided class diagram (ClassDiagram.puml)

**Good luck! 🎵**
