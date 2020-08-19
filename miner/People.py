import time
import os

from miner.Messaging import Messaging
from miner.Friends import Friends
from miner.Person import Person

DATA_PATH = f'{os.getcwd()}/data'

from typing import Union, List, Dict, Callable, Any, NamedTuple


class People:
    """
    Class that manages and represents people from different kind of interactions
    """

    def __init__(self, path: str, friends: Friends, conversations: Messaging) -> None:
        self.data_path: str = path
        self._groups: List = []
        self._data: Dict[str, Person] = self.get_people(friends, conversations)
        self._names: List[str] = self.data.keys()

    @property
    def data(self) -> Dict[str, Person]:
        return self._data
    @property
    def names(self) -> List[str]:
        return list(self.data.keys())

    def get_people(self, friends: Friends, conversations: Messaging) -> Dict[str, Person]:
        friends = self.convert_friends_to_persons(friends)
        convo_partners = self.convert_conversation_partners_to_persons(conversations)
        return self.unify_people(friends, convo_partners)

    @staticmethod
    def convert_friends_to_persons(friends: Friends) -> Dict[str, Person]:
        start = time.time()
        persons = {}
        for i, friend in friends.data.iterrows():
            persons[friend['name']] = Person(name=friend['name'], friend=True)
        print('friends: ', time.time() - start)
        return persons

    @staticmethod
    def convert_conversation_partners_to_persons(conversations: Messaging) -> Dict[str, Person]:
        start = time.time()
        persons = {}
        for name, convo in conversations.private.items():
            persons[name] = Person(
                name=name, messages=convo.data,
                thread_path=convo.metadata.thread_path,
                media_dir=convo.metadata.media_dir
            )

        print('convos: ', time.time() - start)
        return persons

    @staticmethod
    def unify_people(friends, convo_partners):
        for name, friend in friends.items():
            if not convo_partners.get(name):
                convo_partners[name] = friend
            else:
                convo_partners[name] = convo_partners.get(name) + friend
        return convo_partners
