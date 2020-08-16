import time
import os

from miner.Conversations import Conversations
from miner.Friends import Friends

DATA_PATH = f'{os.getcwd()}/data'


class People:
    """
    Class that manages and represents people from different kind of interactions
    # TODO LATER abstractional flaw?! people? person? indie?
    """

    def __init__(self, path=None, name=None):
        self.data_path = path if path else DATA_PATH
        self._groups = []
        self._data = self.get_people(name=name)
        self._names = self.data.keys()

    @property
    def data(self):
        return self._data

    @property
    def names(self):
        return self._names  # if len(self._names) > 1 else self._names[0]

    @property
    def groups(self):
        return self._groups

    def get_people(self, name=None):
        start = time.time()
        friend = Friends(self.data_path + '/friends/friends.json')
        friends = friend.get_people(name=name)
        print('friends: ', time.time() - start)

        start = time.time()
        conversations = Conversations(self.data_path)
        print('convos1: ', time.time() - start)
        start = time.time()
        individuals = conversations.get_people_from_private_messages(name=name)
        print('convos2: ', time.time() - start)

        return self.unify_people(friends, individuals)

    @staticmethod
    def unify_people(friends, convo_partners):
        for person, friend in friends.items():
            if not convo_partners.get(person):
                convo_partners[person] = friend
            else:
                convo_partners[person] = convo_partners.get(person) + friend
        return convo_partners
