from __future__ import annotations

from typing import Union, List, Dict, Callable, Any, NamedTuple
from datetime import datetime
import pandas as pd

from miner.message.conversation_stats import (
    PrivateConversationStats,
    GroupConversationStats,
)
from miner.message.conversations import Conversations
from miner import utils


class ConversationAnalyzer:
    """
    Analyzer for analyzing specific and/or all conversations

    """

    def __init__(self, conversations: Conversations) -> None:
        self.private = conversations.private
        self.group = conversations.group
        self.names: List[str] = list(self.private.keys())

        # self.df: pd.DataFrame = self.get_df(self.private, self.group)
        # self._stats = ConversationStats(self.df)

        self.priv_df: pd.DataFrame = self.get_df(self.private)
        self._priv_stats = PrivateConversationStats(self.priv_df)

        self.group_df: pd.DataFrame = self.get_df(self.group)
        self._group_stats = GroupConversationStats(self.group_df)

    def __str__(self) -> str:
        return f"Analyzing {len(self.priv_df)} messages..."

    @property
    def priv_stats(self) -> PrivateConversationStats:
        return self._priv_stats

    @property
    def stat_sum(self) -> pd.Series:
        return self.priv_stats.stat_sum

    def get_stats(
        self,
        names: str = None,
        subject: str = "all",
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        period: Union[str, datetime] = None,
    ) -> PrivateConversationStats:
        # NOTE: command chaining is also a possibility
        return self.priv_stats.filter(
            names=names, subject=subject, start=start, end=end, period=period
        )

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.get_stats(**kwargs)
        return getattr(stats, attribute)

    # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def most_used_messages(self, top=20) -> pd.Series:
        return self.priv_stats.get_most_used_messages(top)

    # 5. All time: time series: dict of 'y/m/d/h : number of msgs/words/chars (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period="y") -> pd.DataFrame:
        return self.priv_stats.get_grouped_time_series_data(period=period)

    # 6. All time: number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        return self.priv_stats.stat_per_period(period, statistic=statistic)

    # 7. All time: Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic: str = "mc") -> Dict:
        return self.priv_stats.get_ranking_of_partners_by_messages(statistic=statistic)

    @staticmethod
    def get_df(convos) -> pd.DataFrame:
        return utils.stack_dfs(*[convo.data for convo in convos.values()])
