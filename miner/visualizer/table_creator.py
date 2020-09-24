from prettytable import PrettyTable

from miner.visualizer.adapters import TableDataAdapter


class TableCreator:
    def __init__(self, analyzer, config) -> None:
        self._data = TableDataAdapter(analyzer, config)

    def basic_stats(self, kind: str = "private"):
        fields_basic, stats_basic = self._data.get_basic_stats(kind=kind)
        fields_unique, stats_unique = self._data.get_unique_stats(kind=kind)
        fields = fields_basic + fields_unique
        stats = stats_basic + stats_unique
        # title = 'Basic stats'
        table = self._get_table(fields)
        return self._add_content(table, stats)

    def stats_per_timeframe(self, kind: str = "private", timeframe: str = "y"):
        fields, stats_mc = self._data.get_stat_per_timeframe_data(
            kind=kind, timeframe=timeframe, stat="mc"
        )
        _, stats_wc = self._data.get_stat_per_timeframe_data(
            kind=kind, timeframe=timeframe, stat="wc"
        )
        _, stats_cc = self._data.get_stat_per_timeframe_data(
            kind=kind, timeframe=timeframe, stat="cc"
        )

        # title = f"{const.HUMAN_READABLE_PERIODS.get(period)} statistics"
        table = self._get_table(fields)

        table = self._add_content(table, stats_mc)
        table = self._add_content(table, stats_wc)

        return self._add_content(table, stats_cc)

    @staticmethod
    def _get_table(fields):
        table = PrettyTable()
        table.field_names = fields
        return table

    @staticmethod
    def _add_content(table, row):
        beautified = []
        for element in row:
            if isinstance(element, int) or isinstance(element, float):
                beautified.append(f"{element:,}")
        table.add_row(row)
        return table
