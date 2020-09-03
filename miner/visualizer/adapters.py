import pandas as pd

from miner import utils

# TODO make this somehow more generic
class DataAdapter:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.stats = self.get_stats()

    def get_stats(self, **kwargs):
        analyzer = self.analyzer
        return analyzer.stats.filter(**kwargs)


class PlotDataAdapter(DataAdapter):
    """
    Class for adopting statistics data for Visualizer to use.
    """

    def __init__(self, analyzer):
        super().__init__(analyzer)

    def set_up_time_series_data(self, period, stat="text_mc", **kwargs):
        stats = self.get_stats(**kwargs)
        return stats.get_grouped_time_series_data(period)[stat]

    def get_time_series_data(self, period, stat=None, **kwargs):
        index, me, partner = self.get_stat_per_time_data(period, stat)
        utils.generate_date_series(period, start=index[0], end=index[-1])

    def get_stat_per_time_data(self, period, stat="mc", **kwargs):
        me_stat = self.get_stats(subject="me", **kwargs).stat_per_period(
            period, statistic=stat
        )
        partner_stat = self.get_stats(subject="partner", **kwargs).stat_per_period(
            period, statistic=stat
        )
        return list(me_stat.keys()), list(me_stat.values()), list(partner_stat.values())

    def get_ranking_of_friends_by_message_stats(self, stat="mc"):
        ranks_dict = self.analyzer.get_ranking_of_partners_by_convo_stats(
            statistic=stat
        )
        # TODO watch out; might be not working correctly; check upper function
        sorted_dict = utils.sort_dict(
            ranks_dict, func=lambda item: item[1], reverse=True,
        )
        sliced_dict = (
            utils.slice_dict(sorted_dict, 20) if len(sorted_dict) > 20 else sorted_dict
        )
        cleared_dict = utils.remove_items_where_value_is_falsible(sliced_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        return list(df.columns), df.iloc[0]


class TableDataAdapter(DataAdapter):
    def __init__(self, analyzer):
        super().__init__(analyzer)

    def get_basic_stats(self):
        stat_names = [
            "mc",
            "text_mc",
            "media_mc",
            "wc",
            "cc",
        ]
        readables = []
        stats = []
        for name in stat_names:
            readable = utils.STAT_MAP.get(name)
            stat = getattr(self.analyzer.stats, name)
            # yield readable, stat

            readables.append(readable)
            stats.append(stat)
        return readables, stats

    def get_unique_stats(self):
        return (
            ["Unique message", "Unique word"],
            [self.analyzer.priv_stats.unique_mc, self.analyzer.priv_stats.unique_wc,],
        )
        # yield "Unique message", self.analyzer.stats.unique_mc
        # yield "Unique word", self.analyzer.stats.unique_wc

    def get_stat_per_period_data(self, period, stat="mc"):
        dates, counts = [], []
        data = self.analyzer.stats.stat_per_period(period, statistic=stat)
        for date, count in data.items():
            dates.append(date)
            counts.append(count)
        return dates, counts
