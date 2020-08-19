import pandas as pd
import os
from typing import Union, List, Dict, Callable, Any, NamedTuple
from miner.Conversation import Conversation

from miner import utils

DATA_PATH = f'{os.getcwd()}/data'


# TODO rename to MessagingManager or ConversationManager
class Messaging:
    """
    Class for managing and parsing conversations
    """

    def __init__(self, data_path):
        self.path = data_path

        self._directories = ConversationsPaths(self.path)
        self.data_path = f'{data_path}/{utils.MESSAGE_SUBPATH}'

        self._private = self.get_messages(paths=self._directories.private.items(), dir_lister=self.get_json_paths)
        self._group = self.get_messages(paths=self._directories.group.items(), dir_lister=self.get_json_paths)

    @property
    def private(self):
        return self._private

    @property
    def group(self):
        return self._group

    @property
    def directories(self):
        return self._directories

    @staticmethod
    def get_messages(paths, dir_lister):
        name_convo_map = {}
        for name, directory in paths:
            for file in dir_lister(directory):
                convo = Conversation(file)

                if name_convo_map.get(name) is not None:
                    dfs = [name_convo_map[name].data, convo.data]
                    name_convo_map[name].data = pd.concat(dfs).sort_index()
                else:
                    name_convo_map[name] = convo
        return name_convo_map

    @staticmethod
    def get_json_paths(path):
        def get_all_jsons(root, files, extension, contains_string):
            paths = []
            for file_name in files:
                if file_name.endswith(extension) and \
                        contains_string is not None and contains_string in file_name:
                    paths.append(os.path.join(root, file_name))
            return paths

        return utils.walk_directory_and_search(path, get_all_jsons, extension='.json', contains_string='message_')


class ConversationsPaths:
    sub_path = 'messages/inbox'

    def __init__(self, path):
        self.data_path = path
        self.private_paths_map = f'{self.data_path}/{self.sub_path}/private_messages.json'
        self.group_paths_map = f'{self.data_path}/{self.sub_path}/group_messages.json'

        self._private = {}
        self._group = {}

        if not os.path.isfile(self.private_paths_map) or not os.path.isfile(self.group_paths_map):
            self.differentiate_convos()
            self.register_paths()
        self.read_paths()

    @property
    def private(self):
        # TODO maybe a generator
        return self._private

    @property
    def group(self):
        return self._group

    def differentiate_convos(self):
        dirs = self.get_message_dirs()
        for dir in dirs:
            c = Conversation(path=f'{dir}/message_1.json', processors=[])  # NOTE we don't want to process it
            title = Conversation.decode_text(Conversation, c.data.get('title'))  # NOTE this is the raw data
            if c.data.get('thread_type') == 'RegularGroup':
                self._group[title] = dir
            elif c.data.get('thread_type') == 'Regular':
                if title == 'Facebook User':
                    self._private[dir] = dir
                else:
                    self._private[title] = dir

    def get_message_dirs(self):
        return utils.walk_directory_and_search(self.data_path, self.get_parent_directory_of_file, extension='.json',
                                               contains_string='message_1')

    def register_paths(self):
        utils.dump_to_json(self.private, self.private_paths_map)
        utils.dump_to_json(self.group, self.group_paths_map)

    def read_paths(self):
        self._private = utils.read_json(self.private_paths_map)
        self._group = utils.read_json(self.group_paths_map)

    @staticmethod
    def get_parent_directory_of_file(root, files, extension, contains_string):
        for file_name in files:
            if file_name.endswith(extension) and \
                    contains_string is not None and contains_string in file_name:
                return root  # os.path.basename(os.path.normpath(root))

# @staticmethod
# def group_membership():
#     return None
# def filter_by_name(self, name):
#     # TODO what is this function? should not be alive
#     filtered_paths = []
#     names = []
#     if isinstance(name, str):
#         names = [name]
#     elif isinstance(name, list):
#         names = name
#     for name in names:
#         filtered_paths.append(self.private_convo_paths.get(name))
#     return filtered_paths

# def create_individual(self, messages, membership=None):
#     # TODO NO!
#     return Person(
#         name=messages.title,
#         compact=messages.compact_names,
#         messages=messages.df,
#         messages_dir=messages.messages_dir,
#         media_dir=messages.media_dir,
#         member_of=self.group_membership(messages.title) if membership else None,
#     )

# @staticmethod
# def merge_jsons_in_a_directory(path):
#     if os.path.isfile(path) and  path.endswith('.json'):
#         return utils.read_json(path)
#     elif os.path.isdir(path):
#         files = os.listdir(path)
#         data = {}
#         for file in files:
#             if 'message_' in file and file.endswith('.json'):
#                 temp = utils.read_json(os.path.join(path, file))
#                 if not isinstance(temp, dict):
#                     raise SystemExit('not a dict wtf')
#                 if not data:
#                     data = temp
#                 else:
#                     for d, t in zip(data.keys(), temp.keys()):
#                         if isinstance(data[d], str) and isinstance(data[t], str) data[d] == temp[t]:
#                             pass

# def map_private_convo_files(self, msg, file):
#
#     name = msg.title
#     if self.private_convo_paths.get(name):
#         self.private_convo_paths[name].append(file)
#     else:
#         self.private_convo_paths[name] = [file]
#
# def map_group_convo_files(self, msg, file):
#     # TODO should be part of the PrvConvo class methods?!?!
#     for participant in msg.participants:
#         if participant == 'Levente Csőke':
#             continue
#         if self.group_convo_paths.get(file):
#             self.group_convo_paths[file].append(participant)
#         else:
#             self.group_convo_paths[file] = [participant]
