import argparse
import logging
import os

from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.profile_information import ProfileInformation
from miner.utils import utils
from miner.visualizer.plotter import Plotter
from miner.visualizer.table_creator import TableCreator

DATA_PATH = f"{os.getcwd()}/data"


# DATA_PATH = f"{os.getcwd()}/tests/test_data"


class App:
    """
    Entrypoint. Not yet used extensively.
    """

    def __init__(self, path):
        self.path = utils.unzip(path)
        self.configure_logger()
        self.config = self.build_config()

        logging.info("The app has been initialized...")

        self._friends = self.get_friends()
        self._conversations = self.get_conversations()
        self._analyzer = self.get_analyzer()
        # self._people = self.get_people()

    def build_config(self):
        return {"profile": self.profile_information()}

    @staticmethod
    def configure_logger():
        logging.basicConfig(filename="miner.log", level=logging.DEBUG)

    def profile_information(self):
        return ProfileInformation(self.path)

    @property
    def friends(self):
        return self._friends

    @property
    def conversations(self):
        return self._conversations

    @property
    def analyzer(self):
        return self._analyzer

    # TODO correct this
    """@property
    def people(self):
        return self._people """

    def get_friends(self):
        return Friends(f"{self.path}/friends/friends.json")

    def get_conversations(self):
        return Conversations(self.path)

    def get_people(self):
        return People(friends=self.friends, convos=self.conversations,)

    def get_analyzer(self):
        return MessagingAnalyzerManager(self.conversations, self.config)

    def get_plotter(self):
        return Plotter(self.analyzer)

    def create_tables(self):
        tables = TableCreator(self.analyzer)
        tables.print()

    def create_plots(self):
        period = "y"
        stat = "mc"
        names = None
        plotter = self.get_plotter()
        plotter.plot_stat_count_over_time_series(stat=f"{stat}_count", names=names)
        plotter.plot_stat_count_per_time_period(
            period, stat=f"{stat}_count", names=names
        )
        plotter.plot_ranking_of_friends_by_stats(stat=f"{stat}_count")
        plotter.plot_msg_type_ratio()

    def get_messages_ranking(self):
        # TODO or group
        ranking = self.analyzer.private.get_ranking_of_senders_by_convo_stats(
            statistic="mc"
        )
        return ranking


if __name__ == "__main__":
    app = App(DATA_PATH)
    parser = argparse.ArgumentParser(description="Facebook data miner")
    parser.add_argument(
        "-t",
        "--type",
        metavar="type",
        type=str,
        default="tables",
        choices=["tables", "plots"],
        help="Type of output you want to get.",
    )

    args = parser.parse_args()
    output_type = args.type
    if output_type == "tables":
        app.create_tables()
    elif output_type == "plots":
        app.create_plots()
