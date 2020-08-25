from __future__ import annotations
import pandas as pd
import os
from typing import Union, List, Dict, Callable, Any, NamedTuple
from miner.message.conversation import Conversation

from miner import utils

DATA_PATH = f"{os.getcwd()}/data"


class Conversations:
    """
    Class for managing and parsing conversations
    """

    def __init__(self, path: str) -> None:
        self.path: str = path

        paths_factory: ConversationPathFactory = ConversationPathFactory(self.path)

        self._private: Dict[str, Conversation] = self.get_convos(
            directories=paths_factory.get_dirs(ctype="private"),
            dir_lister=self.get_json_paths,
        )
        self._group: Dict[str, Conversation] = self.get_convos(
            directories=paths_factory.get_dirs(ctype="group"),
            dir_lister=self.get_json_paths,
        )

    @property
    def private(self) -> Dict[str, Conversation]:
        return self._private

    @private.setter
    def private(self, data: Dict[str, Conversation]):
        self._private = data

    @property
    def group(self) -> Dict[str, Conversation]:
        return self._group

    def get_convos(
        self, directories: List[str], dir_lister: Callable
    ) -> Dict[str, Conversation]:
        name_convo_map = {}
        for directory in directories:
            jsons = dir_lister(directory)
            name_convo_map = self.merge_convo_files_if_needed(name_convo_map, jsons)
        return name_convo_map

    @staticmethod
    def merge_convo_files_if_needed(
        convo_map: Dict[str, Conversation], jsons: List[str]
    ) -> Dict[str, Conversation]:
        try:
            convo = Conversation(path=next(jsons))
            while json := next(jsons):
                convo += Conversation(path=json)
        except StopIteration:
            # print("WARNING! Convo map is empty!")
            pass
        finally:
            convo_map[convo.metadata.title] = convo
            return convo_map

    @staticmethod
    def get_json_paths(path: str) -> List[str]:

        return utils.walk_directory_and_search(
            path, utils.get_all_jsons, extension=".json", contains_string="message_"
        )


# Note: there should be no need for making this more robust,
# private and group messages are the two only types of messages
class ConversationPathFactory:
    def __init__(self, path: str) -> None:
        self.path = path

    def get_dirs(self, ctype) -> List[str]:
        if ctype not in ("private", "group"):
            raise ValueError("Only `private` and `group` are supported.")
        return ConversationsPaths(path=self.path, ctype=ctype).directories


class ConversationsPaths:
    sub_path: str = "messages/inbox"

    def __init__(self, path: str, ctype: str) -> None:
        if ctype not in ("private", "group"):
            raise ValueError("Only `private` and `group` are supported.")
        self.ctype: str = ctype
        self.thread_type: str = utils.MESSAGE_TYPE_MAP.get(self.ctype)
        self.data_path: str = path

        self.paths_json: str = f"{self.data_path}/{self.sub_path}/{self.ctype}_messages.json"

        self._directories: List[str] = []

        if not os.path.isfile(self.paths_json):
            self.get_convos_paths()
            self.register_paths()
        self.read_paths()

    @property
    def directories(self) -> List[str]:
        return self._directories

    def get_convos_paths(self) -> None:
        directories = self.get_message_dirs(self.data_path)
        for directory in directories:
            convo = Conversation(
                path=f"{directory}/message_1.json", processors=[]
            )  # NOTE we don't want to process it
            if convo.data.get("thread_type") == self.thread_type:
                self._directories.append(directory)

    def register_paths(self) -> None:
        # Question: what if later I want to write this in a database?
        utils.dump_to_json(self.directories, self.paths_json)

    def read_paths(self) -> None:
        self._directories = utils.read_json(self.paths_json)

    @staticmethod
    def get_message_dirs(path: str) -> List[str]:

        return utils.walk_directory_and_search(
            path,
            utils.get_parent_directory_of_file,
            extension=".json",
            contains_string="message_1",
        )
