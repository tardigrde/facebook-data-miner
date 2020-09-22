import argparse
import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from miner.visualizer.adapters import PlotDataAdapter

TEST_DATA_PATH = f"{os.getcwd()}/tests/test_data"


# TEST_DATA_PATH = f"{os.getcwd()}/data"


class Plotter:
    def __init__(self, analyzer, config):
        self._adapter = PlotDataAdapter(analyzer, config)

    def plot_stat_count_over_time_series(
        self, kind: str = "private", stat: str = "mc", **kwargs
    ) -> None:
        # NOTE this only plots time series/year not else.
        index, me, partner = self._adapter.get_stat_per_time_data(
            kind=kind, period="y", stat=stat, **kwargs
        )
        df = pd.DataFrame({"date": index, "me": me, "partner": partner}).set_index(
            "date"
        )

        self._plot_time_series_data(
            df,
            xlabel="Date",
            ylabel=f"Stat count for {stat}",
            title="Stats over time series",
        )

    @staticmethod
    def _plot_time_series_data(df: pd.DataFrame, **kwargs) -> None:
        df.plot(kind="line", linestyle="dashdot", figsize=(16, 5))
        plt.gca().set(**kwargs)
        plt.legend()
        plt.show()

    def plot_stat_count_per_time_period(
        self,
        kind: str = "private",
        period: str = "y",
        stat: str = "mc",
        channels: List[str] = [],
    ):
        index, me, partner = self._adapter.get_stat_per_time_data(
            kind=kind, period=period, stat=stat, channels=channels
        )
        self._plot_stat_per_time(
            index,
            me,
            partner,
            xlabel="Timeperiod",
            ylabel=f"{stat}",
            title="Stats per timeperiod",
        )

    @staticmethod
    def _plot_stat_per_time(index, me, partner, **kwargs):
        # Stacked bar chart
        width = 0.35
        plt.figure(figsize=(12, 12), dpi=100)
        plt.bar(index, me, width, label="me", color="r")
        plt.bar(index, partner, width, label="partner", bottom=me, color="g")
        plt.gca().set(**kwargs)
        plt.legend()
        plt.show()

    def plot_ranking_of_friends_by_stats(self, kind: str = "private", stat: str = "mc"):
        # TODO add filtering possibilities
        y, x = self._adapter.get_ranking_of_friends_by_message_stats(
            kind=kind, stat=stat
        )
        self._plot_horizontal_bar_chart(
            y,
            x,
            xlabel="Stat count",
            ylabel="People",
            title=f"Ranking of people by {stat}",
        )

    @staticmethod
    def _plot_horizontal_bar_chart(y, x, **kwargs):
        y_pos = np.arange(len(y))

        plt.figure(figsize=(12, 12), dpi=100)
        plt.barh(y_pos, x, align="center", tick_label=y)
        plt.gca().invert_yaxis()
        plt.gca().set(**kwargs)  # labels read top-to-bottom
        plt.show()

    def plot_msg_type_ratio(self, kind: str = "private"):
        # TODO private_group
        analyzer = getattr(self._adapter.analyzer, kind)

        percentage = analyzer.stats.percentage_of_media_messages
        data = [100 - percentage, percentage]
        labels = (
            "Text",
            "Media",
        )
        self._plot_pie_chart(
            labels, data,
        )

    @staticmethod
    def _plot_pie_chart(
        labels, data,
    ):
        fig1, ax1 = plt.subplots()
        ax1.pie(data, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

    def plot_convo_type_ratio(self, stat: str = "mc"):
        prv_mc = getattr(getattr(self._adapter.analyzer, "private").stats, stat)
        grp_mc = getattr(getattr(self._adapter.analyzer, "group").stats, stat)

        data = [prv_mc, grp_mc]
        labels = (
            "Private",
            "Group",
        )
        self._plot_pie_chart(
            labels, data,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize chat statistics")
    parser.add_argument(
        "-k",
        "--kind",
        metavar="kind",
        type=str,
        default="private",
        help="private or group",
    )
    parser.add_argument(
        "-t",
        "--typ",
        metavar="typ",
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
    typ = args.typ
    period = args.period
    names = args.names
    stat = args.stat
    from miner.app import App

    app = App(TEST_DATA_PATH)
    v = app._get_plotter()

    if typ == "series":
        # TODO bad visualization!! maybe needs augmentation
        v.plot_stat_count_over_time_series(kind=kind, stat=f"{stat}_count", names=names)
    elif typ == "stats":
        v.plot_stat_count_per_time_period(
            kind=kind, period=period, stat=f"{stat}_count", names=names
        )
    elif typ == "ranking":
        v.plot_ranking_of_friends_by_stats(kind=kind, stat=f"{stat}_count")
    elif typ == "msgtype":
        v.plot_msg_type_ratio(kind=kind)
    elif typ == "convotype":
        v.plot_convo_type_ratio(stat=stat)
