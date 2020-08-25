import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

from miner.visualizer.data_adapter import DataAdapter

from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.message.conversations import Conversations
from miner.people import People
from miner import utils

TEST_DATA_PATH = f"{os.getcwd()}/tests/test_data"


# TEST_DATA_PATH = f'{os.getcwd()}/data'


class Visualizer:
    def __init__(self, path):
        self.path = path
        self.analyzer = self.get_analyzer()
        self.stats = self.get_stats()
        pass

    def get_analyzer(self):
        convos = Conversations(path=self.path)
        return ConversationAnalyzer(convos)

    def get_stats(self, **kwargs):
        analyzer = self.get_analyzer()
        return analyzer.get_stats(**kwargs)

    def set_up_time_series_data(self, period, stat="msg_count", **kwargs):
        stats = self.get_stats(**kwargs)
        return stats.get_conversation_statistics(period)[stat]

    def setup_data_for_all_subjects(self, period, stat=None, **kwargs):
        all_data = self.set_up_time_series_data(
            period, stat=stat, subject="all", **kwargs
        )
        me_data = self.set_up_time_series_data(
            period, stat=stat, subject="me", **kwargs
        )
        partner_data = self.set_up_time_series_data(
            period, stat=stat, subject="partner", **kwargs
        )
        df = pd.concat([all_data, me_data, partner_data], axis=1).fillna(0)
        df.columns = ["all", "me", "partner"]
        return df

    def plot_time_series_data_of_messages(self, period, **kwargs):
        df = self.setup_data_for_all_subjects(period, **kwargs)
        self.plot_time_series(df, title=name, stat=stat)

    @staticmethod
    def plot_time_series(
        df, title="Time series analysis", xlabel="Date", stat="msg_count"
    ):
        ylabel = f"Stat for {stat}"
        df.plot(kind="line", linestyle="dashdot", figsize=(16, 5))
        plt.gca().set(xlabel=xlabel, ylabel=ylabel)
        plt.title(title)  # does not work
        plt.legend()
        plt.show()

    def bar_plot_stat_per_time_period(self, period, stat="msg_count", **kwargs):
        me_stat = self.get_stats(subject="me", **kwargs).stat_per_period(
            period, statistic=stat
        )
        partner_stat = self.get_stats(subject="partner", **kwargs).stat_per_period(
            period, statistic=stat
        )
        me_stat, partner_stat = utils.unify_dict_keys(me_stat, partner_stat)
        df = pd.DataFrame(
            {
                "date": list(me_stat.keys()),
                "me": list(me_stat.values()),
                "partner": list(partner_stat.values()),
            }
        )
        df = df.set_index("date")
        self.plot_stat_per_time(df, stat=stat)

    @staticmethod
    def plot_stat_per_time(
        df, stat="msg_count", title="Stat per timeperiod", xlabel="Timeperiod", dpi=100
    ):
        # Stacked bar chart
        width = 0.35
        ylabel = f"Stat for {stat}"
        plt.figure(figsize=(12, 12), dpi=dpi)
        plt.bar(list(df.index), list(df.me), width, label="me", color="r")
        plt.bar(
            list(df.index),
            list(df.partner),
            width,
            label="partner",
            bottom=list(df.me),
            color="g",
        )
        plt.gca().set(xlabel=xlabel, ylabel=ylabel)
        plt.title(title)  # does not work
        plt.legend()
        plt.show()

    def plot_ranking_of_friends_by_message_stats(self, stat="msg_count"):
        analyzer = self.get_analyzer()
        ranks_dict = analyzer.get_ranking_of_partners_by_messages(statistic=stat)
        sorted_dict = utils.sort_dict(
            ranks_dict, func=lambda item: item[1], reverse=True
        )
        sliced_dict = (
            utils.slice_dict(sorted_dict, 20) if len(sorted_dict) > 20 else sorted_dict
        )
        cleared_dict = utils.remove_items_where_value_is_falsible(sliced_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        self.horizontal_bar_chart(df, stat=stat)

    @staticmethod
    def horizontal_bar_chart(
        df, stat="msg_count", title="Ranking of friends {}", dpi=100
    ):
        people = list(df.columns)
        y_pos = np.arange(len(people))
        performance = df.iloc[0]

        plt.figure(figsize=(12, 12), dpi=dpi)
        plt.barh(y_pos, performance, align="center", tick_label=people)
        plt.gca().invert_yaxis()  # labels read top-to-bottom
        plt.title(title.format(stat))
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize chat statistics")
    parser.add_argument(
        "-p",
        "--period",
        metavar="period",
        type=str,
        default="y",
        help="One of {y|m|d|h}, standing for yearly, monthly, daily and hourly breakdown of statisctics.",
    )
    parser.add_argument(
        "-n",
        "--name",
        metavar="name",
        type=str,
        default=None,
        help="A person's name if you only want data filtered only for them.",
    )
    parser.add_argument(
        "-s",
        "--stat",
        metavar="stat",
        type=str,
        default="msg",
        help="One of {msg|word|char}, indicating which statistics do you want to get.",
    )

    # TODO add possibility for adding dates from the command line
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    args = parser.parse_args()
    period = args.period
    name = args.name
    stat = args.stat
    v = Visualizer(path=TEST_DATA_PATH)
    # TODO bad visualization!! maybe needs augmentation
    # v.plot_time_series_data_of_messages(period, names=name, stat=f'{stat}_count')
    # v.bar_plot_stat_per_time_period(period, names=name, stat=f'{stat}_count')
    # v.plot_ranking_of_friends_by_message_stats()
