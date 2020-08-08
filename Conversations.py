import os
from FacebookData import FacebookData
import pandas as pd

from datetime import datetime

MESSAGE_SUBPATH = 'messages/inbox'


class Conversations:
    def __init__(self, data_path):
        self.data_path = f'{data_path}/{MESSAGE_SUBPATH}'

    def get_people(self):
        json_paths = self.walk_directory_and_search('.json')
        return self.extract_names_from_convos(json_paths)

    def walk_directory_and_search(self, extension):
        paths = []
        for root, dirs, files in os.walk(self.data_path):
            for name in files:
                if name.endswith(extension):
                    paths.append(os.path.join(root, name))
        return paths

    @staticmethod
    def extract_names_from_convos(jsons):
        name_data_map = {}
        count = 0
        for file in jsons:
            msg = Messages(file)
            for participant in msg.participants:
                key = participant if msg.ttype == 'Regular' else f'group_{count}'
                if key == 'Facebook User':  # TODO ?? what to do with this??
                    continue
                if name_data_map.get(key) and key.startswith(
                        'group'):  # making sure run only once even if it is a group
                    continue
                if name_data_map.get(key):
                    dfs = [name_data_map[key]['messages'], msg.df]
                    name_data_map[key]['messages'] = pd.concat(dfs, ignore_index=True)
                else:
                    name_data_map[key] = {
                        'title': msg.title,
                        'compact_name': msg.compact_names,  # TODO is list ok for if length is  only  1??
                        #'participants': msg.participants + ['Levente Csőke'],
                        'participants': msg.participants,
                        'messages': msg.df,
                        'friend': None,
                        'messages_dir': msg.messages_dir,
                        'media_dir': msg.media_dir
                    }
            if msg.ttype == 'RegularGroup':
                count += 1

        return name_data_map


class Messages(FacebookData):
    def __init__(self, json_path):
        super().__init__(json_path)
        self.to_df()
        self.set_date_as_index()

    def to_df(self):
        self._df = pd.DataFrame(self.decoded.get('messages'))

    def set_date_as_index(self):
        # TODO maybe not needed; could calculate real time
        date_series = self._df.timestamp_ms.apply(self.ts_to_date)
        self._df = self._df.set_index(date_series).iloc[::-1]

    @property
    def names(self):
        return pd.DataFrame(self.participants)[0]

    @property
    def participants(self):
        participants = self.decoded.get('participants')
        # TODO I should be IN
        # but this breaks stuff at TestMessagingAnalyzer
        return [p.get('name') for p in participants if p.get('name') != 'Levente Csőke']
        #return [p.get('name') for p in participants if p.get('name')]

    @property
    def title(self):
        return self.decoded.get('title')

    @property
    def ttype(self):
        return self.decoded.get('thread_type')

    @property
    def messages_dir(self):
        thread_path = self.decoded.get('thread_path')
        if not thread_path.startswith('inbox/'):
            raise ValueError('Something is not okay.')
        # TODO here or in the upper function where we extract names
        return thread_path.split('/')[1].lower()

    @property
    def media_dir(self):
        # todo what should the path contain
        for media in ['photos', 'gifs', 'files', 'videos', 'audio']:
            if media in self._df.columns:
                media_in_msg = list(self._df[media][self._df[media].notnull()])
                # if len(media_in_msg) > 1:  # TODO is this ok. i think it is. think multiple photos sent once
                #    print('Media in msg is bigger than 1')
                uri = media_in_msg[0][0].get('uri')
                return os.path.dirname(os.path.dirname(uri))
        return None

    @staticmethod
    def ts_to_date(date):
        return datetime.fromtimestamp(date / 1000)  # .strftime('%Y-%m-%d')
