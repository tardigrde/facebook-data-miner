import logging
import os
from typing import Dict, Union

from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.profile_information import ProfileInformation
from miner.utils import const, utils


class App:
    """
    Entrypoint for miner package.
    """

    def __init__(self, path: Union[str, None] = None):
        if not path:
            config = utils.read_yaml(
                os.path.join(
                    f"{os.path.dirname(os.path.dirname(__file__))}",
                    "configuration.yml",
                )
            )
            path = config.get("general").get("DATA_PATH")

        self._path = utils.unzip(path)

        self._configure_logger()
        self._config = self._build_config()

        logging.info("The app has been initialized...")

        self._friends = self._get_friends()
        self._conversations = self._get_conversations()
        self._analyzer = self._get_analyzer()
        self._people = self._get_people()

    @property
    def friends(self) -> Friends:
        return self._friends

    @property
    def conversations(self) -> Conversations:
        return self._conversations

    @property
    def analyzer(self) -> MessagingAnalyzerManager:
        return self._analyzer

    @property
    def people(self) -> People:
        return self._people

    @property
    def config(self) -> Dict[str, ProfileInformation]:
        return self._config

    @property
    def profile_information(self) -> ProfileInformation:
        return ProfileInformation(self._path)

    def _get_friends(self) -> Friends:
        return Friends(os.path.join(f"{self._path}", *const.FRIENDS_PATH))

    def _get_conversations(self) -> Conversations:
        return Conversations(self._path)

    def _get_analyzer(self) -> MessagingAnalyzerManager:
        return MessagingAnalyzerManager(self._conversations, self._config)

    def _get_people(self) -> People:
        return People(friends=self._friends, conversations=self._conversations)

    def _build_config(self) -> Dict[str, ProfileInformation]:
        return {"profile": self.profile_information}

    @staticmethod
    def _configure_logger() -> None:
        logging.basicConfig(level=logging.WARNING)
