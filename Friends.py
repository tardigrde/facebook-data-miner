import pandas as pd
import os
from FacebookData import FacebookData
from utils import accents_map


class Friends(FacebookData):

    def __init__(self, *args):
        super().__init__(*args)

        # self.path = 'data/friends'
        # self.json_path = f'{self.path}/friends.json'

        self.to_df()

    def get_people(self):
        names = {}
        for name, compact in zip(self.names, self.compact_names):
            names[name] = {
                'title': name,
                'compact_name': compact,
                'messages': None,
                'friend': True,
                'participants': None,
                'messages_dir': None,
                'media_dir': None
            }
        return names

    def to_df(self):
        self._df = pd.DataFrame(self.decoded.get('friends'))

    @property
    def names(self):
        return self.df.name
