import os
from miner.Group import Group
from miner.Individual import Individual
from miner.FacebookData import FacebookData
import pandas as pd
from miner import utils
from datetime import datetime


class Conversations:
    def __init__(self, data_path):
        self.indie_convo_paths = []
        self.group_convo_paths = []
        self.deleted_user_convo_paths = []

        self.data_path = f'{data_path}/{utils.MESSAGE_SUBPATH}'
        self.order_paths()

    def order_paths(self):
        json_paths = utils.walk_directory_and_search(self.data_path, '.json')
        self.differentiate_paths(json_paths)

    def differentiate_paths(self, jsons):
        for file in jsons:
            msg = Messages(file)
            if msg.title == 'Facebook User':
                self.deleted_user_convo_paths.append(file)
            elif msg.ttype == 'RegularGroup':
                self.group_convo_paths.append(file)
            elif msg.ttype == 'Regular':
                self.indie_convo_paths.append(file)
            else:
                raise ValueError('Should not happen!')

    def get_people_from_private_messages(self, name=None, membership=True):
        name_data_map = {}
        paths = self.indie_convo_paths
        if name is not None:
            paths = self.filter_by_name(name)
        for file in paths:
            messages = Messages(file)
            name = messages.title
            if name_data_map.get(name) is not None:
                dfs = [name_data_map[name].messages, messages.df]
                name_data_map[name].messages = pd.concat(dfs).sort_index()
            else:
                # TODO we may also want to get group messages where name is present
                name_data_map[name] = self.create_individual(messages, membership=membership)
        return name_data_map

    def filter_by_name(self, name):
        filtered_paths = []
        compact_name = None if name is None else utils.replace_accents(name.lower())
        for path in self.indie_convo_paths:
            if compact_name in os.path.basename(os.path.dirname(os.path.normpath(path))):
                filtered_paths.append(path)
        return filtered_paths

    def create_individual(self, messages, membership=None):
        return Individual(
            name=messages.title, title=messages.title,  # TODO depracate one of (name, title)
            compact=messages.compact_names,
            messages=messages.df,
            messages_dir=messages.messages_dir,
            media_dir=messages.media_dir,
            member_of=self.group_membership(messages.title) if membership else None,
        )

    @staticmethod
    def fill_data_map(message):
        return {
            'title': message.title,
            'compact_name': message.compact_names,
            # 'participants': msg.participants + ['Levente Csőke'],
            'participants': message.participants,
            'messages': message.df,
            'friend': None,
            'messages_dir': message.messages_dir,
            'media_dir': message.media_dir
        }

    @staticmethod
    def group_membership(name):
        return None

    @staticmethod
    def json_is_a_group_msg(file):
        msg = Messages(file)
        return msg.ttype == 'RegularGroup'


class Messages(FacebookData):
    def __init__(self, json_path):
        super().__init__(json_path)
        self.to_df('messages')
        self.set_date_as_index()

    @property
    def names(self):
        return pd.DataFrame(self.participants)[0]

    @property
    def participants(self):
        participants = self.decoded.get('participants')
        # TODO I should be IN
        # but this breaks stuff at TestMessagingAnalyzer
        return [p.get('name') for p in participants if p.get('name') != 'Levente Csőke']
        # return [p.get('name') for p in participants if p.get('name')]

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
            raise ValueError('Field `thread_path` should start with `inbox/`.')
        return thread_path.split('inbox/')[1]

    @property
    def media_dir(self):
        for media in utils.MEDIA_DIRS:
            if media in self._df.columns:
                media_in_msg = list(self._df[media][self._df[media].notnull()])
                uri = media_in_msg[0][0].get('uri')
                return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]

    def set_date_as_index(self):
        date_series = self._df.timestamp_ms.apply(self.ts_to_date)
        self._df = self._df.set_index(date_series).iloc[::-1]

    @staticmethod
    def ts_to_date(date):
        return datetime.fromtimestamp(date / 1000)  # .strftime('%Y-%m-%d')
