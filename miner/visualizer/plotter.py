import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

from typing import Union, List, Dict, Callable, Any, NamedTuple

# from miner.visualizer.adapters import DataAdapter
from miner.visualizer.adapters import PlotDataAdapter

TEST_DATA_PATH = f"{os.getcwd()}/tests/test_data"


# TEST_DATA_PATH = f"{os.getcwd()}/data"


class Plotter:
    def __init__(self, analyzer):
        self.adapter = PlotDataAdapter(analyzer)

    def plot_stat_count_over_time_series(self, stat: str, **kwargs) -> None:
        # NOTE this only plots time series/year not else.
        index, me, partner = self.adapter.get_stat_per_time_data("y", stat, **kwargs)
        df = pd.DataFrame({"date": index, "me": me, "partner": partner,})
        df = df.set_index("date")

        self.plot_time_series_data(
            df,
            xlabel="Date",
            ylabel=f"Stat count for {stat}",
            title="Stats over time series",
        )

    @staticmethod
    def plot_time_series_data(df: pd.DataFrame, **kwargs) -> None:
        df.plot(kind="line", linestyle="dashdot", figsize=(16, 5))
        plt.gca().set(**kwargs)
        plt.legend()
        plt.show()

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
            title=f"Ranking of people by {stat}",
        )

    @staticmethod
    def plot_horizontal_bar_chart(y, x, **kwargs):
        y_pos = np.arange(len(y))

        plt.figure(figsize=(12, 12), dpi=100)
        plt.barh(y_pos, x, align="center", tick_label=y)
        plt.gca().invert_yaxis()
        plt.gca().set(**kwargs)  # labels read top-to-bottom
        plt.show()

    def plot_msg_type_ratio(self):
        percentage = self.adapter.analyzer.priv_stats.percentage_of_media_messages
        data = [100 - percentage, percentage]
        labels = (
            "Text",
            "Media",
        )
        self.plot_pie_chart(
            labels, data,
        )

    @staticmethod
    def plot_pie_chart(
        labels, data,
    ):
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize chat statistics")
    parser.add_argument(
        "-k",
        "--kind",
        metavar="kind",
        type=str,
        default="ranking",
        help="One of {series|stats|ranking|type}, standing for time series, stats per period, ranking of friends by messages and type of messages",
    )
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
    kind = args.kind
    period = args.period
    names = args.names
    stat = args.stat
    from miner.app import App

    app = App(TEST_DATA_PATH)
    v = app.get_plotter()
    if kind == "series":
        # TODO bad visualization!! maybe needs augmentation
        v.plot_stat_count_over_time_series(stat=f"{stat}_count", names=names)
    elif kind == "stats":
        v.plot_stat_count_per_time_period(period, stat=f"{stat}_count", names=names)
    elif kind == "ranking":
        v.plot_ranking_of_friends_by_stats(stat=f"{stat}_count")
    elif kind == "msgtype":
        v.plot_msg_type_ratio()
    elif kind == "convotype":
        pass
