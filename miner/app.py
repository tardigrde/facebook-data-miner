import logging
import os

from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.profile_information import ProfileInformation
from miner.utils import utils

# DATA_PATH = f"{os.path.dirname(os.path.dirname(__file__))}/data"


DATA_PATH = f"{os.path.dirname(os.path.dirname(__file__))}/tests/test_data"


class App:
    """
    Entrypoint.
    """

    def __init__(self, path: str = None):
        if not path:
            config = utils.read_yaml(
                f"{os.path.dirname(os.path.dirname(__file__))}/configuration.yml"
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
    def friends(self):
        return self._friends

    @property
    def conversations(self):
        return self._conversations

    @property
    def analyzer(self):
        return self._analyzer

    @property
    def people(self):
        return self._people

    @property
    def config(self):
        return self._config

    @property
    def profile_information(self):
        return ProfileInformation(self._path)

    def _get_friends(self):
        return Friends(f"{self._path}/friends/friends.json")

    def _get_conversations(self):
        return Conversations(self._path)

    def _get_people(self):
        return People(friends=self._friends, conversations=self._conversations)

    def _get_analyzer(self):
        return MessagingAnalyzerManager(self._conversations, self._config)

    def _build_config(self):
        return {"profile": self.profile_information}

    @staticmethod
    def _configure_logger():
        logging.basicConfig(level=logging.WARNING)
