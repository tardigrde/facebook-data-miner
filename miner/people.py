from typing import Union, List, Dict, Callable, Any, NamedTuple
import time
import os

from miner.message.conversations import Conversations
from miner.friends import Friends
from miner.person import Person

DATA_PATH = f"{os.getcwd()}/data"


class People:
    """
    Class that manages and represents people from different kind of interactions.
    """

    def __init__(self, **kwargs) -> None:
        self.source_map = self.get_source_map()
        self._data: Dict[str, Person] = self.get_data_from_source(**kwargs)

    def __iter__(self):
        # NOTE: not sure if this is needed. Wanted to try out object as its own iterator.
        return PeopleIterator(self)

    @property
    def data(self) -> Dict[str, Person]:
        return self._data

    @property
    def names(self) -> List[str]:
        return list(self._data.keys())

    def get_source_map(self) -> Dict[str, Callable]:
        return {
            "friends": self.convert_friends_to_persons,
            "conversations": self.convert_conversation_partners_to_persons,
        }

    def get_data_from_source(self, **kwargs) -> Dict[str, Person]:
        data = {}
        for key, source in kwargs.items():
            other = data
            this = self.source_map[key](source)
            data = self.unify_people(this, other)
        return data

    @staticmethod
    def unify_people(this, other) -> Dict[str, Any]:
        for name, person in this.items():
            if not other.get(name):
                other[name] = person
            else:
                other[name] = other.get(name) + person
        return other

    @staticmethod
    def convert_friends_to_persons(friends: Friends) -> Dict[str, Person]:
        start = time.time()
        persons = {}
        for i, friend in friends.data.iterrows():
            persons[friend["name"]] = Person(name=friend["name"], friend=True)
        print("friends: ", time.time() - start)
        return persons

    @staticmethod
    def convert_conversation_partners_to_persons(
        conversations: Conversations,
    ) -> Dict[str, Person]:
        start = time.time()
        persons = {}
        for name, convo in conversations.private.items():
            persons[name] = Person(
                name=name,
                messages=convo.data,
                thread_path=convo.metadata.thread_path,
                media_dir=convo.metadata.media_dir,
            )
        print("convos: ", time.time() - start)
        return persons


class PeopleIterator:
    def __init__(self, container):
        self.container = container
        self.n = -1
        self.max = len(self.container.names)

    def __next__(self):
        self.n += 1
        if self.n > self.max:
            raise StopIteration
        return self.container.data[self.container.names[self.n]]

    def __iter__(self):
        return self
