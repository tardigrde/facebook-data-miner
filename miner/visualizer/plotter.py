import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from miner.visualizer.adapters import PlotDataAdapter


class Plotter:
    def __init__(self, analyzer, config):
        self._adapter = PlotDataAdapter(analyzer, config)

    def plot_stat_count_over_time_series(
        self,
        kind: str = "private",
        stat: str = "mc",
        channels: str = None,
        participants: str = None,
        **kwargs,
    ) -> None:
        # NOTE this only plots time series/year not else.
        index, me, partner = self._adapter.get_stat_per_time_data(
            channels=channels,
            participants=participants,
            kind=kind,
            period="y",
            stat=stat,
            **kwargs,
        )
        df = pd.DataFrame({"date": index, "me": me, "partner": partner}).set_index("date")

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
        timeframe: str = "y",
        stat: str = "mc",
        channels: str = None,
        participants: str = None,
        **kwargs,
    ):
        index, me, partner = self._adapter.get_stat_per_time_data(
            kind=kind,
            timeframe=timeframe,
            stat=stat,
            channels=channels,
            participants=participants,
            **kwargs,
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

    def plot_ranking_of_friends_by_stats(
        self,
        kind: str = "private",
        stat: str = "mc",
        channels: str = None,
        participants: str = None,
    ):
        y, x = self._adapter.get_ranking_of_friends_by_message_stats(
            kind=kind, stat=stat, channels=channels, participants=participants
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

    def plot_msg_type_ratio(
        self,
        kind: str = "private",
        channels: str = None,
        participants: str = None,
        senders: str = None,
        **kwargs,
    ):
        analyzer = getattr(self._adapter.analyzer, kind).filter(
            channels=channels, participants=participants
        )

        percentage = analyzer.stats.filter(
            senders=senders, **kwargs
        ).percentage_of_media_messages
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
