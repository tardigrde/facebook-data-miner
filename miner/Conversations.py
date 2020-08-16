import pandas as pd
import os

from miner.Messages import Messages
from miner.Individual import Individual

from miner import utils


class Conversations:
    """
    Class for managing and parsing conversations
    """

    def __init__(self, data_path):
        self.private_convo_paths = {}
        self.group_convo_paths = {}  # TODO LATER fill this as well
        self.deleted_user_convo_paths = []  # NOTE these are collected but not yet used

        self.data_path = f'{data_path}/{utils.MESSAGE_SUBPATH}'
        self.order_paths()

    def order_paths(self):
        paths_map = f'{self.data_path}/private_messages.json'
        if os.path.isfile(paths_map):
            self.read_paths(paths_map)
            return
        json_paths = utils.walk_directory_and_search(self.data_path, '.json', contains_string='message_')
        self.differentiate_paths(json_paths)
        self.register_paths()

    def differentiate_paths(self, jsons):
        for file in jsons:
            msg = Messages(file)
            if msg.title == 'Facebook User':
                self.deleted_user_convo_paths.append(msg.messages_dir)
            elif msg.ttype == 'RegularGroup':
                self.map_group_convo_files(msg, file)
            elif msg.ttype == 'Regular':
                # self.private_convo_paths[msg.title] = msg.messages_dir
                self.map_private_convo_files(msg, file)
            else:
                raise ValueError('Should not happen!')

    def register_paths(self):
        utils.dump_to_json(self.private_convo_paths, f'{self.data_path}/private_messages.json')

    def read_paths(self, file):
        self.private_convo_paths = utils.read_json(file)
        print()

    def map_private_convo_files(self, msg, file):
        name = msg.title
        if self.private_convo_paths.get(name):
            self.private_convo_paths[name].append(file)
        else:
            self.private_convo_paths[name] = [file]

    def map_group_convo_files(self, msg, file):
        for participant in msg.participants:
            if participant == 'Levente Csőke':
                continue
            if self.group_convo_paths.get(file):
                self.group_convo_paths[file].append(participant)
            else:
                self.group_convo_paths[file] = [participant]

    def get_people_from_private_messages(self, name=None, membership=True):
        name_data_map = {}
        convo_path_map = self.filter_by_name(name) if name is not None else self.private_convo_paths.values()
        for paths in convo_path_map:
            for file in paths:
                messages = Messages(file)
                name = messages.title
                if name_data_map.get(name) is not None:
                    dfs = [name_data_map[name].messages, messages.df]
                    name_data_map[name].messages = pd.concat(dfs).sort_index()
                else:
                    name_data_map[name] = self.create_individual(messages, membership=membership)
        return name_data_map

    def filter_by_name(self, name):
        filtered_paths = []
        names = []
        if isinstance(name, str):
            names = [name]
        elif isinstance(name, list):
            names = name
        for name in names:
            filtered_paths.append(self.private_convo_paths.get(name))
        return filtered_paths

    def create_individual(self, messages, membership=None):
        return Individual(
            name=messages.title,
            compact=messages.compact_names,
            messages=messages.df,
            messages_dir=messages.messages_dir,
            media_dir=messages.media_dir,
            member_of=self.group_membership(messages.title) if membership else None,
        )

    @staticmethod
    def group_membership(name):
        return None

    def get_people_from_group_messages(self):
        pass
