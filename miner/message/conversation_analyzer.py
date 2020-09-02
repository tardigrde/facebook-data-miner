from __future__ import annotations

from typing import Union, List, Dict, Callable, Any, NamedTuple
from datetime import datetime
import pandas as pd

import numpy as np
from miner.message.conversation_stats import (
    ConversationStats,
    PrivateConversationStats,
    GroupConversationStats,
)
from miner.message.conversations import Conversations
from miner.message.conversation import Conversation
from miner import utils


class MessagingAnalyzerManager:
    def __init__(self, conversations: Conversations) -> None:
        self.conversations = conversations
        self.private_messaging_analyzer = PrivateMessagingAnalyzer(
            conversations.private
        )
        self.group_messaging_analyzer = GroupMessagingAnalyzer(
            conversations.group, conversations.group_convo_map
        )

    @property
    def private(self):
        return self.private_messaging_analyzer

    @property
    def group(self):
        return self.group_messaging_analyzer

    def how_much_i_speak_in_private_with_group_members(self):
        pass

    def all_interactions(self):  # ->new ranking
        # means private and all the group chats?
        pass

    def is_priv_or_group_msg_first(self):
        # *needs private, all the groups that the partner is in
        pass

    def get_stats_together(self):
        pass

    def get_who_I_have_private_convo_with(self):  # * private convos
        # TODO maybe a new data structure -> PersonsConversation
        # OR
        pass

    def get_ratio_of_who_i_have_private_convo_with(self):  # *private convos
        # *needs participants, and all the private convos with them
        pass

    def get_how_many_friends_in_group_message(self):  # * needs people
        # TODO stat does not belong here
        pass


class MessagingAnalyzer:
    def __init__(self, data: Dict[str, Conversation]) -> None:
        self.data = data
        self.df: pd.DataFrame = self.get_df(self.data)

    @property
    def stats(self):
        return self._stats

    @property
    def stat_sum(self) -> pd.Series:
        return self.stats.stat_sum

    def filter(self):  # TODO
        pass

    def get_stats(
        self,
        names: str = None,
        subject: str = "all",
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
        period: Union[str, datetime] = None,
    ) -> ConversationStats:
        return self.stats.filter(
            names=names, subject=subject, start=start, end=end, period=period
        )

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.get_stats(**kwargs)
        return getattr(stats, attribute)

    @staticmethod
    def get_df(convos) -> pd.DataFrame:
        return utils.stack_dfs(*[convo.data for convo in convos.values()])

    def get_how_many_created_by_me(self,):
        raise NotImplementedError()


class PrivateMessagingAnalyzer(MessagingAnalyzer):
    # private convo data
    def __init__(self, data: Dict[str, Conversation]) -> None:
        super().__init__(data)
        self._stats = PrivateConversationStats(self.df)

    # TODO cannot these functions be in both priv and group/?????

    # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def most_used_messages(self, top=20) -> pd.Series:
        return self.stats.get_most_used_messages(top)

    # 5. All time: time series: dict of 'y/m/d/h : number of msgs/words/chars (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period="y") -> pd.DataFrame:
        return self.stats.get_grouped_time_series_data(period=period)

    # 6. All time: number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        return self.stats.stat_per_period(period, statistic=statistic)

    # 7. All time: Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic: str = "mc") -> Dict:
        return self.stats.get_ranking_of_partners_by_messages(statistic=statistic)

    def get_how_many_created_by_me(self,):
        # *private_convo specific dfs' first row
        pass


class GroupMessagingAnalyzer(MessagingAnalyzer):
    # group convo data
    def __init__(
        self, data: Dict[str, Conversation], group_convo_map: Dict[str, List]
    ) -> None:
        super().__init__(data)
        self._stats = GroupConversationStats(self.df)
        self.group_convo_map = group_convo_map  # TODO

    def get_all_groups_for_one_person(self, name):  # *one group's participants
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def group_mean_size(self):  # *all group's size
        sizes = []
        for g in self.data.values():
            size = len(g.metadata.participants)
            sizes.append(size)
        return sum(sizes) / len(sizes)

    def max_group_size(
        self,
    ):  # *all group's size #TODO do we need this as well or only the name of the group
        sizes = []
        for g in self.data.values():
            size = len(g.metadata.participants)
            sizes.append(size)
        return max(sizes)

    def get_how_many_created_by_me(self,):
        # *group_convo specific dfs' first row
        pass

    def get_stat_per_participant(self):
        # TODO what stats. there are plenty.
        # like all of them? mc, wc, cc byt filtering
        pass


# class ConversationAnalyzer:
#     """
#     Analyzer for analyzing specific and/or all conversations
#
#     """
#
#     def __init__(self, conversations: Conversations) -> None:
#         self.conversations = conversations
#
#         # self.private = PrivateMessagingAnalyzer#conversations.private
#         self.private = conversations.private
#         self.groups = conversations.group
#         self.names: List[str] = list(self.private.keys())
#
#         # self.df: pd.DataFrame = self.get_df(self.private, self.group)
#         # self._stats = ConversationStats(self.df)
#
#         self.priv_df: pd.DataFrame = self.get_df(self.private)
#         self._priv_stats = PrivateConversationStats(self.priv_df)
#
#         self.group_df: pd.DataFrame = self.get_df(self.groups)
#         self._group_stats = GroupConversationStats(self.group_df)
#
#     def __str__(self) -> str:
#         return f"Analyzing {len(self.priv_df)} messages..."
#
#     @property
#     def priv_stats(self) -> PrivateConversationStats:
#         return self._priv_stats
#
#     @property
#     def stat_sum(self) -> pd.Series:
#         return self.priv_stats.stat_sum
#
#     @property
#     def group_stats(self) -> GroupConversationStats:
#         return self._group_stats
#
#     def get_stats(
#             self,
#             kind: str = "private",
#             names: str = None,
#             subject: str = "all",
#             start: Union[str, datetime] = None,
#             end: Union[str, datetime] = None,
#             period: Union[str, datetime] = None,
#     ) -> ConversationStats:
#         if kind == "private":
#             return self.priv_stats.filter(
#                 names=names, subject=subject, start=start, end=end, period=period
#             )
#         elif kind == "group":
#             return self.group_stats.filter(
#                 names=names, subject=subject, start=start, end=end, period=period
#             )
#
#     def get_stat_count(
#             self, kind: str = "private", attribute: str = "mc", **kwargs
#     ) -> int:
#         stats = self.get_stats(kind=kind, **kwargs)
#         return getattr(stats, attribute)
#
#     # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
#     def most_used_messages(self, top=20) -> pd.Series:
#         return self.priv_stats.get_most_used_messages(top)
#
#     # 5. All time: time series: dict of 'y/m/d/h : number of msgs/words/chars (also sent/got) for user/all convos'
#     def get_grouped_time_series_data(self, period="y") -> pd.DataFrame:
#         return self.priv_stats.get_grouped_time_series_data(period=period)
#
#     # 6. All time: number of messages sent/got on busiest period (by year/month/day/hour)
#     def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
#         return self.priv_stats.stat_per_period(period, statistic=statistic)
#
#     # 7. All time: Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
#     def get_ranking_of_partners_by_messages(self, statistic: str = "mc") -> Dict:
#         return self.priv_stats.get_ranking_of_partners_by_messages(statistic=statistic)
#
#     @staticmethod
#     def get_df(convos) -> pd.DataFrame:
#         return utils.stack_dfs(*[convo.data for convo in convos.values()])
