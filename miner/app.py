#!/home/levente/anaconda3/envs/fb/bin/python
import logging
import os
import traceback
from datetime import datetime
from typing import List, Union, Any

from fire import Fire

from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.profile_information import ProfileInformation
from miner.utils import utils
from miner.visualizer.adapters import AnalyzerFacade, GenericAnalyzerFacade
from miner.visualizer.plotter import Plotter
from miner.visualizer.table_creator import TableCreator

# DATA_PATH = f"{os.getcwd()}/data"


DATA_PATH = f"{os.path.dirname(os.path.dirname(__file__))}/tests/test_data"


class App:
    """
    Entrypoint.
    """

    def __init__(self, path):
        self._path = utils.unzip(path)
        self._configure_logger()
        self._config = self._build_config()

        logging.info("The app has been initialized...")

        self._friends = self._get_friends()
        self._conversations = self._get_conversations()
        self._analyzer = self._get_analyzer()
        self._people = self._get_people()

    def friends(self, sort="date", dates=True, output=None):
        """
        Mi van

        @param sort: a
        @param dates: b
        @param output: c
        @return: list of friends, sorted by @sort, with dates of making friend if @dates is True,
        saved in a csv or json file if @output is a valid path.
        """
        return self._friends.get(sort=sort, dates=dates, output=output)

    def conversations(
        self,
        kind: str = "private",
        channels: str = None,
        cols: List[str] = None,
        output: str = None,
    ):
        """

        @param kind:
        @param channels:
        @param cols:
        @param output:
        @return:
        """
        return self._conversations.get(
            kind=kind, channels=channels, cols=cols, output=output
        )

    def analyzer(
        self,
        kind: str = None,
        channels: str = None,
        participants: str = None,
        senders: str = None,
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        period: str = None,
    ) -> Union[GenericAnalyzerFacade, AnalyzerFacade]:
        if kind is None:
            return GenericAnalyzerFacade(self._analyzer)
        return AnalyzerFacade(
            self._analyzer,
            kind=kind,
            channels=channels,
            participants=participants,
            senders=senders,
            start=start,
            end=end,
            period=period,
        )

    def report(self) -> TableCreator:
        return TableCreator(self._analyzer, self._config)

    def plot(self) -> Plotter:
        # NOTE saving images to output is yet to be implemented
        return Plotter(self._analyzer, self._config)

    def people(self):
        return self._people.get()

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
        return {"profile": self.profile_information()}

    @staticmethod
    def _configure_logger():
        logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    app = App(DATA_PATH)
    # Fire(app, name="Facebook-Data-Miner")
    try:
        Fire(app, name="Facebook-Data-Miner")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logging.error(f"An exception has happened:\n{e}")
