from __future__ import annotations
from typing import Union, List, Dict, Callable, Any, NamedTuple
import pandas as pd
from dataclasses import dataclass
from miner import utils


@dataclass
class Person:
    """
    Class for holding a person's data the user ever interacted with
    """
    name: str
    friend: bool = None
    compact_name: str = None
    messages: pd.DataFrame = pd.DataFrame()
    thread_path: str = None
    media_dir: str = None
    member_of: List[str] = None

    def __post_init__(self) -> None:
        self.compact_name = utils.replace_accents(self.name.lower())

    def __add__(self, other: Person) -> Person:
        return Person(
            name=self.name if self.name else other.name,
            compact_name=self.compact_name if self.compact_name else other.compact_name,
            friend=self.friend if self.friend else other.friend,
            messages=self.messages if len(self.messages) else other.messages,
            thread_path=self.thread_path if self.thread_path else other.thread_path,
            media_dir=self.media_dir if self.media_dir else other.media_dir,
            member_of=self.member_of if self.member_of else other.member_of
        )

# class Person:
#     """
#     Class for holding a person's data the user ever interacted with
#     """
#
#
#     # TODO this is actually only a data schema. could be a dataframe. should be a dataframe
#
#     def __init__(self, name=None, compact=None, messages=None, friend=None, messages_dir=None,
#                  media_dir=None,
#                  member_of=None):
#         self._name = name
#         self._compact_name = compact
#         self._messages = messages
#         self._friend = friend
#         self._messages_dir = messages_dir
#         self._media_dir = media_dir
#         self._member_of = member_of
#
#     def __repr__(self):
#         return f'{self.name}, messages: {self.messages}'
#
#     def __add__(self, other):
#         return Person(
#             name=self.name if self.name else other.name,
#             friend=self.friend if self.friend else other.friend,
#             compact=self.compact_name if self.compact_name else other.compact_name,
#             messages=self.messages if len(self.messages) else other.messages,
#             messages_dir=self.messages_dir if self.messages_dir else other.messages_dir,
#             media_dir=self.media_dir if self.media_dir else other.media_dir,
#             member_of=self.member_of if self.member_of else other.member_of
#         )
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def messages(self):
#         return self._messages
#
#     @messages.setter
#     def messages(self, df):
#         self._messages = df
#
#     @property
#     def friend(self):
#         return self._friend
#
#     @property
#     def media_dir(self):
#         return self._media_dir
#
#     @property
#     def messages_dir(self):
#         return self._messages_dir
#
#     @property
#     def compact_name(self):
#         return self._compact_name
#
#     @property
#     def member_of(self):
#         return self._member_of
