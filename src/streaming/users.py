"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""
from streaming import *

from datetime import date

from streaming import ListeningSession


class User:

    def __init__(self, user_id: str, name: str, age: int):
        """

        :type user_id: str
        :type name: str
        :type age: int
        """
        self.sessions: list[ListeningSession] = []
        self.age = age
        self.name = name
        self.user_id = user_id

    def add_session(self, session: ListeningSession):
        self.sessions.append(session)

    def total_listening_seconds(self) -> int:
        return sum([s.duration_listened_seconds for s in self.sessions])

    def total_listening_minutes(self) -> float:
        return sum([s.duration_listened_minutes() for s in self.sessions])

    def unique_tracks_listened(self) -> set[str]:
        return set([s.track.track_id for s in self.sessions])


class FreeUser(User):
    """
    FreeUser("u1", "User", age=20)
    """
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)


class PremiumUser(User):
    """
    PremiumUser("u1", "User", age=20, subscription_start=date(2023, 1, 1))
    """
    def __init__(self, user_id: str, name: str, age: int, subscription_start: date):
        super().__init__(user_id, name, age)
        self.age = age
        self.subscription_start = subscription_start


class FamilyAccountUser(User):
    sub_users: list[FamilyMember]

    def __init__(self, user_id: str, name: str, age:int):
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user: FamilyMember):
        self.sub_users.append(sub_user)

    def all_members(self) -> list[User]:
        return [self] + self.sub_users


class FamilyMember(User):
    """
    FamilyMember("u2", "Child", age=16, parent=family)
    """
    def __init__(self, user_id: str, name: str, age:int, parent:FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent = parent

