from Individual import Individual
from Conversations import Conversations
from Friends import Friends

# from Me import Me
DATA_PATH = '/home/levente/projects/facebook-data-miner/data'
import time
from Group import Group


# TODO we dont need both data and individuals... or??

class People:
    def __init__(self, path=None):
        self.data_path = path if path else DATA_PATH
        self._names = []
        self._individuals = {}
        self._groups = []
        self._data = self.get_people()  # TODO is this supposed to be here or elsewhere
        self.to_individuals()  # TODO is this supposed to be here or elsewhere

    @property
    def data(self):
        return self._data

    @property
    def names(self):
        return self._names

    @property
    def individuals(self):
        return self._individuals

    @property
    def groups(self):
        return self._groups

    def get_people(self):
        start = time.time()
        friends = Friends(self.data_path + '/friends/friends.json')
        people1 = friends.get_people()
        print('friends: ', time.time() - start)

        # TODO LATER too slow
        # takes about 30 secs both
        # read it once, store it in DB OR?
        start = time.time()
        conversations = Conversations(self.data_path)
        people2 = conversations.get_people()
        print('convos: ', time.time() - start)

        return self.unify_people(people1, people2)

    def to_individuals(self):  # TODO maybe rather split_convos or differentiate_convos
        start = time.time()
        for person, data in self._data.items():
            if person.startswith('group'):
                g = Group(name=data.get('name'), title=data.get('title'), messages=data.get('messages'),
                          compact=data.get('compact_name'), messages_dir=data.get('messages_dir'),
                          media_dir=data.get('media_dir'), members=None)
                self._groups.append(g)
            else:
                indie = Individual(name=person, title=data.get('title'), messages=data.get('messages'),
                                   compact=data.get('compact_name'), messages_dir=data.get('messages_dir'),
                                   media_dir=data.get('media_dir'), member_of=None)
                self._names.append(person)
                self._individuals[person] = indie
        print('indies: ', time.time() - start)

    @staticmethod
    def unify_people(friends, convos):
        for person, data in friends.items():
            if not convos.get(person):
                convos[person] = data
            convos[person]['friend'] = True
        return convos

# if __name__ == '__main__':
#     p = People()
