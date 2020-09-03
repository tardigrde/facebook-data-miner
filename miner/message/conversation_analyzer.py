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


# TODO
# maybeeeee the private and group stuff can be merged in one
# actually makes only a little sense to subclass it
# just so you dont use conditionals in convo_stats that says if self.groups or smthg like that


class MessagingAnalyzerManager:
    def __init__(self, conversations: Conversations) -> None:
        self.conversations = conversations
        self.private_messaging_analyzer = PrivateMessagingAnalyzer(
            conversations.private
        )
        # maybe move group_convo_map creation to here, not conversations
        self.group_messaging_analyzer = GroupMessagingAnalyzer(
            conversations.group, conversations.group_convo_map
        )

    @property
    def private(self):
        return self.private_messaging_analyzer

    @property
    def group(self):
        return self.group_messaging_analyzer

    def people_i_have_private_convo_with(self):
        return self.private_messaging_analyzer.data.keys()

    def people_i_have_group_convo_with(self):
        return self.group_messaging_analyzer.group_convo_map.keys()

    def get_who_i_have_private_convo_with_from_a_group(self, group_name):
        if not group_name:
            return

        have = []
        participants = self.group_messaging_analyzer.filter(
            names=group_name
        ).participants
        for p in participants:
            if p in self.private_messaging_analyzer.data is not None:
                have.append(p)
        return have

    def how_much_i_speak_in_private_with_group_members(self, group_name):
        person_private_stats_map = {}
        participants = self.group_messaging_analyzer.filter(
            names=group_name
        ).participants
        for p in self.get_who_i_have_private_convo_with_from_a_group(group_name):
            person_private_stats_map[p] = self.private_messaging_analyzer.filter(
                names=p
            ).stats.mc
        return person_private_stats_map

    def all_interactions(self, name):
        # means private and all the group chats?
        # needs: private, and all the groups partner is in
        private = self.private_messaging_analyzer.filter(names=name)
        group = self.group_messaging_analyzer.filter(names=name)
        return private, group

    def is_priv_msg_first_then_group(self, name):
        # *needs private.start, all the group.start that the partner is in
        private = self.private_messaging_analyzer.filter(names=name)
        group = self.group_messaging_analyzer.filter(names=name)
        g_start_times = []
        for g in group:
            start_time = self.group_messaging_analyzer.filter(groups=g).stats.start
            g_start_times.append(start_time)

        return any([private.start > group_start for group_start in g_start_times])

    def get_stats_together(self, name):
        # needs all the messages from private and all groups; create a new  DF from that
        private = self.private_messaging_analyzer.filter(names=name).stats.df
        group = self.group_messaging_analyzer.filter(names=name)
        groups = [
            self.group_messaging_analyzer.filter(groups=g).stats.df for g in group
        ]
        df = utils.stack_dfs(private, *groups)
        return PrivateConversationStats(
            df
        )  # TODO violation!!!!! this is why we need to remove difference


class MessagingAnalyzer:
    def __init__(self, data: Dict[str, Conversation]) -> None:
        self.data = data
        self.df: pd.DataFrame = self.get_df(self.data)

    @property
    def stats(self):
        return self._stats

    @property
    def portion_of_contribution(self):
        ranking_dict = self.get_ranking_of_partners_by_convo_stats()
        hundred = sum(list(ranking_dict.values()))
        return {name: value * 100 / hundred for name, value in ranking_dict.items()}

    @property
    def most_contributed(self):
        return list(self.portion_of_contribution.items())[0]

    @property
    def least_contributed(self):
        return list(self.portion_of_contribution.items())[-1]

    def filter(self):
        raise NotImplementedError()

    def get_stats_per_partner(self):
        raise NotImplementedError()

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.stats.filter(**kwargs)
        return getattr(stats, attribute)

    def get_ranking_of_partners_by_convo_stats(self, statistic: str = "mc") -> Dict:
        count_dict = {}
        if len(self.stats_per_partner) == 1:
            raise utils.TooFewPeopleError("Can't rank one person.")
        for name, stats in self.stats_per_partner.items():
            count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
            count_dict = utils.sort_dict(
                count_dict, func=lambda item: item[1], reverse=True
            )
        return count_dict

    @staticmethod
    def get_df(convos) -> pd.DataFrame:
        return utils.stack_dfs(*[convo.data for convo in convos.values()])


class PrivateMessagingAnalyzer(MessagingAnalyzer):
    # private convo data
    def __init__(self, data: Dict[str, Conversation]) -> None:
        super().__init__(data)
        self._stats = PrivateConversationStats(self.df)
        self._stats_per_partner = self.get_stats_per_partner()

    @property
    def stats_per_partner(self):
        return self._stats_per_partner

    @property
    def number_of_convos_created_by_me(self):
        return sum([stat.created_by_me for stat in self.stats_per_partner.values()])

    @utils.string_kwarg_to_list_converter("names")
    def filter(self, names=None):
        if not names:
            return self
        data = {name: self.data[name] for name in names}
        return PrivateMessagingAnalyzer(data)

    def get_stats_per_partner(self):
        return {
            name: PrivateConversationStats(convo.data)
            for name, convo in self.data.items()
        }


class GroupMessagingAnalyzer(MessagingAnalyzer):
    # group convo data
    def __init__(
        self, data: Dict[str, Conversation], group_convo_map: Dict[str, List]
    ) -> None:
        super().__init__(data)
        self._stats = GroupConversationStats(self.df)
        self.group_convo_map = group_convo_map  # TODO

        self._stats_per_conversation = self.get_stats_per_conversation()
        self._stats_per_partner = self.get_stats_per_partner()

    @property
    def participants(self):
        # super set of self.stats.names
        participants = []
        for k, g in self.data.items():
            participants += g.metadata.participants
        return sorted(list(set(participants)))

    @property
    def number_of_convos_created_by_me(self):
        return sum(
            [stat.created_by_me for stat in self.stats_per_conversation.values()]
        )

    @property
    def stats_per_conversation(self):
        return self._stats_per_conversation

    @property
    def stats_per_partner(self):
        return self._stats_per_partner

    @property
    def min_group_size(self):
        sizes = self.get_group_sizes(self.data)
        return min(sizes.values())

    @property
    def mean_group_size(self):
        sizes = self.get_group_sizes(self.data)
        return sum(sizes.values()) / len(sizes.values())

    @property
    def max_group_size(self):
        sizes = self.get_group_sizes(self.data)
        return max(sizes.values())

    def get_all_groups_for_one_person(self, name):
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def get_stats_per_conversation(self):
        return {
            name: GroupConversationStats(convo.data)
            for name, convo in self.data.items()
        }

    def get_stats_per_partner(self) -> Dict[str, GroupConversationStats]:
        stat_per_participant = {}
        for name in self.participants:
            stat_per_participant[name] = self.stats.filter(sender=name)
        # looks like the following:
        # self => whatever names where filtered (either 1 or more groups)
        # self.stats => all time stats for the filtered names
        # self.stats.names => should be all the real names, that are part of the/these group message(s)
        # self.stats.filter(names=name) we only create stats for one member of the group messages(s)
        return stat_per_participant

    # TODO myabe move this to a filterer class?!?!?!
    @utils.string_kwarg_to_list_converter("names")
    @utils.string_kwarg_to_list_converter("groups")
    def filter(self, names=None, groups=None):  # NOTE filtering by name, not group name
        if names is None and groups is None:
            return self
        if names is not None:
            data, group_convo_map = self.filter_by_name(
                self.data, self.group_convo_map, names
            )
        if groups is not None:
            data, group_convo_map = self.filter_by_group_name(
                self.data, self.group_convo_map, groups
            )
        return GroupMessagingAnalyzer(data, group_convo_map)

    @staticmethod
    def filter_by_name(data, group_convo_map, names):
        new_data = {}
        for key, g in data.items():
            if list(set(g.metadata.participants) & set(names)):
                new_data[key] = g
        new_group_convo_map = {name: group_convo_map[name] for name in names}
        return new_data, new_group_convo_map

    @staticmethod
    def filter_by_group_name(data, group_convo_map, groups):
        new_group_convo_map = {}
        new_data = {name: data[name] for name in groups}
        for key, group_list in group_convo_map.items():
            if list(set(group_list) & set(groups)):
                new_group_convo_map[key] = group_list
        return new_data, new_group_convo_map

    @staticmethod
    def get_group_sizes(data):
        sizes = {}
        for k, g in data.items():
            size = len(g.metadata.participants)
            sizes[k] = size
        return sizes


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
