from typing import Union, List, Dict, Callable, Any, NamedTuple
from miner.message.conversations import Conversations
from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.people import People
from miner.friends import Friends

from miner import utils


class Report:
    def __init__(self, analyzer) -> None:
        self.content = []
        self.data = ReportDataAdapter(analyzer)
        self.transform_data()

    def transform_data(self):
        self.fill_content()
        # self.get_ranking_data()

    def print(self):
        for key, value in self.content:
            print(f"{key}: {value}")

    def add_content(self, text, stat):
        self.content.append((text, stat,))

    def get_ranking_data(self):
        ranking = self.data.get_ranking(stat="msg_count")
        self.add_content("")

    def fill_content(self):
        for name, stat in self.data.get_basic_stats():
            self.add_content(f"{name} count", f"{stat:,}")
        for name, stat in self.data.get_unique_stats():
            self.add_content(f"{name} count", f"{stat:,}")
        print(40 * "-")
        self.fill_stat_per_period_data(stat="msg_count")
        print(40 * "-")
        self.fill_stat_per_period_data(stat="word_count")
        print(40 * "-")
        self.fill_stat_per_period_data(stat="char_count")
        print(40 * "-")

    def fill_stat_per_period_data(self, stat="msg_count"):
        self.add_content("Time period statistic", utils.STAT_MAP.get(stat))
        for time, stat in self.data.get_stat_per_period_data(stat=stat):
            self.add_content(time, stat)


class ReportDataAdapter:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def get_ranking(self, stat="msg_count"):
        return self.analyzer.get_ranking_of_friends_by_message_stats(stat=stat)

    def get_basic_stats(self):
        stat_names = [
            "msg_count",
            "text_msg_count",
            "media_count",
            "word_count",
            "char_count",
        ]
        for name in stat_names:
            readable = utils.STAT_MAP.get(name)
            stat = self.analyzer.stat_sum[name]
            yield readable, stat

    def get_unique_stats(self):
        yield "Unique message", self.analyzer.stats.unique_msg_count
        yield "Unique word", self.analyzer.stats.unique_word_count

    def get_stat_per_period_data(self, stat="msg_count"):
        for period in ["y", "m", "d", "h"]:
            # for period in ['y',]:
            data = self.analyzer.stat_per_period(period, statistic=stat)
            for year, count in data.items():
                yield year, f"{count:,}"
