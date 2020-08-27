from typing import Union, List, Dict, Callable, Any, NamedTuple
from miner.message.conversations import Conversations
from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.people import People
from miner.friends import Friends
from miner.visualizer.adapters import TableDataAdapter

from prettytable import PrettyTable

from miner import utils


class TableCreator:
    def __init__(self, analyzer) -> None:
        self.content = []
        self.tables = {}
        self.data = TableDataAdapter(analyzer)
        self.transform_data()

    def transform_data(self):
        self.fill_content()
        # self.get_ranking_data()

    def print(self):
        # for key, value in self.content:
        #     print(f"{key}: {value}")
        for key, value in self.tables.items():
            print(key)
            print(value)

    def get_table(self, fields):
        x = PrettyTable()
        x.field_names = fields
        return x

    def add_content(self, table, row):
        # self.content.append((text, stat,)
        table.add_row(row)
        return table

    def table_creator(self, data_getter, title):
        if callable(data_getter):
            fields, stats = data_getter()
        else:
            fields, stats = data_getter
        table = self.get_table(fields)
        table = self.add_content(table, stats)
        self.tables[title] = table

    def fill_content(self):
        # TODO better design
        self.table_creator(self.data.get_basic_stats, "Basic stat count")
        self.table_creator(self.data.get_unique_stats, "...")

        # TODO needs row identifier (msg,word, char count)
        # TODO needs separaton at every 3rd number
        for period, title, in zip(
            ["y", "m", "d", "h"], ["Yearly", "Monthly", "Daily", "Hourly"]
        ):
            title = f"{title} statistics"
            fields, stats = self.data.get_stat_per_period_data(period, stat="msg_count")
            self.table_creator((fields, stats), title)
            fields, stats = self.data.get_stat_per_period_data(
                period, stat="word_count"
            )
            self.add_content(self.tables[title], stats)
            fields, stats = self.data.get_stat_per_period_data(
                period, stat="char_count"
            )
            self.add_content(self.tables[title], stats)

        # for name, stat in self.data.get_basic_stats():
        #     self.add_content(f"{name} count", f"{stat:,}")
        # for name, stat in self.data.get_unique_stats():
        #     self.add_content(f"{name} count", f"{stat:,}")
        # print(40 * "-")
        # self.fill_stat_per_period_data(stat="msg_count")
        # print(40 * "-")
        # self.fill_stat_per_period_data(stat="word_count")
        # print(40 * "-")
        # self.fill_stat_per_period_data(stat="char_count")
        # print(40 * "-")

    def fill_stat_per_period_data(self, period, stat="msg_count"):
        self.add_content("Time period statistic", utils.STAT_MAP.get(stat))
        for time, stat in self.data.get_stat_per_period_data(period, stat=stat):
            self.add_content(time, stat)
