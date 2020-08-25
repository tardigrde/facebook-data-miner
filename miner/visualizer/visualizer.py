import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

from typing import Union, List, Dict, Callable, Any, NamedTuple

from miner.visualizer.data_adapter import DataAdapter

TEST_DATA_PATH = f"{os.getcwd()}/tests/test_data"


# TEST_DATA_PATH = f'{os.getcwd()}/data'


class Visualizer:
    dpi: int = 100
    square_shape: tuple = (
        12,
        12,
    )
    rectangular_shape: tuple = (16, 5)

    def __init__(self, path):
        self.adapter = DataAdapter(path)

    def plot_stat_count_over_time_series(self, stat: str, names: []) -> None:
        plottables = self.adapter.get_time_series_data(
            stat=stat, subjects=["all", "me", "partner"], names=names
        )
        self.plot_time_series_data(
            plottables,
            xlabel="Date",
            ylabel=f"Stat count for {stat}",
            title="Stats over time series",
        )

    @staticmethod
    def plot_time_series_data(plottables: List, **kwargs) -> None:
        # df.plot(kind="line", linestyle="dashdot", figsize=(16, 5))
        # for plottable in plottables:
        #    plt.plot(plottable)
        # plt.gca().set(**kwargs)
        # plt.legend()
        # plt.show()
        pass

    def plot_stat_count_per_time_period(self, period, stat: str, names: []):
        index, me, partner = self.adapter.get_stat_per_time_data(
            period, stat, names=names
        )
        self.plot_stat_per_time(
            index,
            me,
            partner,
            xlabel="Timeperiod",
            ylabel=f"{stat}",
            title="Stats per timeperiod",
        )

    @staticmethod
    def plot_stat_per_time(index, me, partner, **kwargs):
        # Stacked bar chart
        width = 0.35
        plt.figure(figsize=(12, 12), dpi=100)
        plt.bar(index, me, width, label="me", color="r")
        plt.bar(index, partner, width, label="partner", bottom=me, color="g")
        plt.gca().set(**kwargs)
        plt.legend()
        plt.show()

    def plot_ranking_of_friends_by_stats(self, stat: str):
        # TODO add filtering possibilities
        y, x = self.adapter.get_ranking_of_friends_by_message_stats(stat=stat)
        self.plot_horizontal_bar_chart(
            y,
            x,
            xlabel="Stat count",
            ylabel="People",
            title="Ranking of people my stats",
        )

    @staticmethod
    def plot_horizontal_bar_chart(y, x, **kwargs):
        y_pos = np.arange(len(y))

        plt.figure(figsize=(12, 12), dpi=100)
        plt.barh(y_pos, x, align="center", tick_label=y)
        plt.gca().invert_yaxis()
        plt.gca().set(**kwargs)  # labels read top-to-bottom
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
        "--names",
        metavar="names",
        type=str,
        default=None,
        help="A person's name or people's name if you only want data filtered only for them.",
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
    names = args.names
    stat = args.stat
    v = Visualizer(path=TEST_DATA_PATH)

    # TODO bad visualization!! maybe needs augmentation
    # v.plot_stat_count_over_time_series(stat=f'{stat}_count', names=names)
    # TODO broken
    # v.plot_stat_count_per_time_period(period, stat=f'{stat}_count', names=names)
    #
    v.plot_ranking_of_friends_by_stats(stat=f"{stat}_count")
