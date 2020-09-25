from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from miner.utils import utils


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
        self.compact_name = utils.replace_accents(self.name.lower()).replace(" ", "")

    def __add__(self, other: Person) -> Person:
        if not self.name == other.name:
            raise ValueError("The two person has different names!")
        return Person(
            name=self.name,
            compact_name=self.compact_name if self.compact_name else other.compact_name,
            friend=self.friend if self.friend else other.friend,
            messages=self.messages if len(self.messages) else other.messages,
            thread_path=self.thread_path if self.thread_path else other.thread_path,
            media_dir=self.media_dir if self.media_dir else other.media_dir,
            member_of=self.member_of if self.member_of else other.member_of,
        )

    def __repr__(self) -> str:
        return f"Name: {self.name}, friend: {self.friend}, msg directory: {self.thread_path}"
