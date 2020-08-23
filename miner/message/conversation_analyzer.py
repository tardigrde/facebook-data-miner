from __future__ import annotations
import pandas as pd

from miner.message.conversations import Conversations
from miner.message.conversation_stats import ConversationStats

from miner import utils
from typing import Union, List, Dict, Callable, Any, NamedTuple


class ConversationAnalyzer:
    """
    Analyzer for analyzing specific and/or all conversations

    """

    def __init__(self, conversations: Conversations) -> None:
        self.private = conversations.private
        self.names: List[str] = list(self.private.keys())

        self.df: pd.DataFrame = self.get_df(self.private)
        self._stats = ConversationStats(self.df)

    def __str__(self) -> Union[str, List[str]]:
        return f'Analyzing {len(self.df)} messages...'

    @property
    def stats(self) -> ConversationStats:
        return self._stats

    def get_stats(self, names=None, subject='all', start=None, end=None, period=None):
        return self.stats.get_filtered_stats(names=names, subject=subject, start=start, end=end, period=period)

    def get_stat_count(self, attribute='msg_count', **kwargs):
        stats = self.get_stats(**kwargs)
        return getattr(stats, attribute)

    # TODO this should be all time stats interface
    # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def most_used_messages(self, top=20):
        return self.stats.get_most_used_messages(top)

    # 5. All time: time series: dict of 'y/m/d/h : number of msgs/words/chars (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period='y'):
        return self.stats.get_grouped_time_series_data(period=period)

    # 6. All time: number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period, statistic='msg_count'):
        return self.stats.stat_per_period(period, statistic=statistic)

    # 7. All time: Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic='msg_count'):
        return self.stats.get_ranking_of_partners_by_messages(statistic=statistic)

    @staticmethod
    def get_df(convos):
        return utils.stack_dfs(*[convo.data for convo in convos.values()])
