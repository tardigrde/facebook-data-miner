import os
import argparse
import time
from typing import Union, List, Dict, Callable, Any, NamedTuple

from miner.message.conversations import Conversations
from miner.people import People
from miner.friends import Friends
from miner.visualizer.table_creator import TableCreator
from miner.visualizer.plotter import Plotter
from miner.message.messaging_analyzer import MessagingAnalyzerManager

DATA_PATH = f"{os.getcwd()}/data"
# DATA_PATH = f"{os.getcwd()}/tests/test_data"


class App:
    """
    Entrypoint. Not yet used extensively.
    """

    def __init__(self, path):
        print("The app has been initialized...")
        self.path = path
        self._friends = self.get_friends()
        self._conversations = self.get_conversations()
        self._analyzer = self.get_analyzer()
        # self._people = self.get_people()

    # TODO add properties because from notebook e.g. get_analyzer has to recalculate everything
    @property
    def friends(self):
        return self._friends

    @property
    def conversations(self):
        return self._conversations

    @property
    def analyzer(self):
        return self._analyzer

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
        return MessagingAnalyzerManager(self.conversations)

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
