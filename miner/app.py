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

# DATA_PATH = f"{os.getcwd()}/data"
DATA_PATH = f"{os.getcwd()}/tests/test_data"


def get_how_many_friends_in_group_message():  # * needs people
    # TODO stat does not belong here
    # OR
    # maybe inject people here but not so straightforward
    pass


class App:
    """
    Entrypoint. Not yet used extensively.
    """

    def __init__(self, path):
        print("The app has been started...")
        self.path = path

    def get_friends(self):
        return Friends(f"{self.path}/friends/friends.json")

    def get_conversations(self):
        return Conversations(self.path)

    def get_people(self):
        return People(
            friends=self.get_friends(), conversations=self.get_conversations()
        )

    def get_analyzer(self):
        return MessagingAnalyzerManager(self.get_conversations())

    def get_plotter(self):
        return Plotter(self.get_analyzer())

    def create_tables(self):
        tables = TableCreator(self.get_analyzer())
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
        analyzer = self.get_analyzer()
        ranking = analyzer.get_ranking_of_partners_by_convo_stats(statistic="mc")
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
