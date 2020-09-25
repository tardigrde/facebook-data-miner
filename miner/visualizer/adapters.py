import pandas as pd

from miner.utils import utils, const


class DataAdapter:
    def __init__(self, analyzer, config):
        self.analyzer = analyzer
        self.config = config

    @property
    def private(self):
        return self.analyzer.private

    @property
    def group(self):
        return self.analyzer.group

    def get_private_stats(self, channels=None, senders=None, **kwargs):
        return self.private.filter(channels=channels, senders=senders).stats.filter(
            **kwargs
        )

    def get_group_stats(self, channels=None, senders=None, **kwargs):
        return self.group.filter(channels=channels, senders=senders).stats.filter(
            **kwargs
        )


class TableDataAdapter(DataAdapter):
    def __init__(self, analyzer, config):
        super().__init__(analyzer, config)

    def get_basic_stats(self, kind: str = "private"):

        titles = []
        stats = []
        for name in const.STAT_MAP.keys():
            readable = const.STAT_MAP.get(name)
            stat = getattr(getattr(self.analyzer, kind).stats, name)
            titles.append(readable)
            stats.append(stat)
        return titles, stats

    def get_unique_stats(self, kind: str = "private"):
        analyzer = getattr(self.analyzer, kind)
        return (
            ["Unique message", "Unique word"],
            [analyzer.stats.unique_mc, analyzer.stats.unique_wc,],
        )

    def get_stat_per_timeframe_data(
        self, kind: str = "private", timeframe: str = "y", stat: str = "mc"
    ):
        dates, counts = [""], [const.STAT_MAP.get(stat)]
        data = getattr(self.analyzer, kind).stats.stats_per_timeframe(
            timeframe, statistic=stat
        )
        for date, count in data.items():
            dates.append(date)
            counts.append(count)
        return dates, counts


class PlotDataAdapter(DataAdapter):
    """
    Class for adopting statistics data for Visualizer to use.
    """

    def __init__(self, analyzer, config):
        super().__init__(analyzer, config)

    def set_up_time_series_data(self, timeframe, stat="text_mc", **kwargs):
        stats = self.analyzer.stats.filter(**kwargs)
        return stats.get_grouped_time_series_data(timeframe)[stat]

    def get_time_series_data(
        self, kind: str = "private", timeframe: str = "y", stat=None, **kwargs
    ):
        index, me, partner = self.get_stat_per_time_data(
            kind=kind, timeframe=timeframe, stat=stat, **kwargs
        )
        utils.generate_date_series(
            self.config.get("profile").registration_timestamp,
            timeframe,
            start=index[0],
            end=index[-1],
        )

    def get_stat_per_time_data(
        self,
        kind: str = "private",
        timeframe: str = "y",
        stat: str = "mc",
        channels: str = None,
        participants: str = None,
        **kwargs
    ):
        analyzer = getattr(self.analyzer, kind).filter(
            channels=channels, participants=participants
        )
        me_stat = analyzer.stats.filter(senders="me", **kwargs).stats_per_timeframe(
            timeframe, statistic=stat
        )
        partner_stat = analyzer.stats.filter(
            senders="partner", **kwargs
        ).stats_per_timeframe(timeframe, statistic=stat)
        return list(me_stat.keys()), list(me_stat.values()), list(partner_stat.values())

    def get_ranking_of_friends_by_message_stats(
        self,
        kind: str = "private",
        stat="mc",
        channels: str = None,
        participants: str = None,
    ):
        analyzer = getattr(self.analyzer, kind).filter(
            channels=channels, participants=participants
        )
        ranking = analyzer.get_ranking_of_people_by_convo_stats(statistic=stat, top=20)
        sorted_dict = utils.sort_dict(
            ranking.get("count"), func=lambda item: item[1], reverse=True,
        )

        cleared_dict = utils.remove_items_where_value_is_falsible(sorted_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        return list(df.columns), df.iloc[0]
