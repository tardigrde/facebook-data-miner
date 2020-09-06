from __future__ import annotations

from typing import Union, List, Dict, Callable, Any, NamedTuple, Tuple
from datetime import datetime
import pandas as pd

import copy
import numpy as np
from miner.message.conversation_stats import ConversationStats
from miner.message.conversations import Conversations
from miner.message.conversation import Conversation
from miner import utils


class MessagingAnalyzerManager:
    def __init__(self, conversations: Conversations) -> None:
        self.conversations = conversations
        self.private_messaging_analyzer = MessagingAnalyzer(
            conversations.private, "private"
        )
        # maybe move group_convo_map creation to here, not conversations
        self.group_messaging_analyzer = MessagingAnalyzer(conversations.group, "group")

    @property
    def private(self) -> MessagingAnalyzer:
        return self.private_messaging_analyzer

    @property
    def group(self) -> MessagingAnalyzer:
        return self.group_messaging_analyzer

    def people_i_have_private_convo_with(self) -> List[str]:
        return list(self.private_messaging_analyzer.data.keys())

    def people_i_have_group_convo_with(self) -> List[str]:
        return list(self.group_messaging_analyzer.group_convo_map.keys())

    def get_who_i_have_private_convo_with_from_a_group(
        self, group_name: str
    ) -> List[str]:
        have = []
        participants = self.group_messaging_analyzer.filter(
            senders=group_name
        ).participants
        for p in participants:
            if p in self.private_messaging_analyzer.data is not None:
                have.append(p)
        return have

    def how_much_i_speak_in_private_with_group_members(
        self, group_name: str
    ) -> Dict[str, int]:
        person_private_stats_map = {}
        # participants = self.group_messaging_analyzer.filter(
        #     senders=group_name
        # ).participants
        for p in self.get_who_i_have_private_convo_with_from_a_group(group_name):
            person_private_stats_map[p] = self.private_messaging_analyzer.filter(
                channels=p
            ).stats.mc
        return person_private_stats_map

    def all_interactions(
        self, name: str
    ) -> Tuple[ConversationStats, ConversationStats]:
        # means private and all the group chats?
        # needs: private, and all the groups partner is in
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(senders=name)
        return private, group

    def is_priv_msg_first_then_group(self, name: str) -> bool:
        # *needs private.start, all the group.start that the partner is in
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(senders=name)
        g_start_times = []
        for g in group:
            start_time = self.group_messaging_analyzer.filter(channels=g).stats.start
            g_start_times.append(start_time)

        return any([private.start > group_start for group_start in g_start_times])

    def get_stats_together(self, name: str) -> ConversationStats:
        # needs all the messages from private and all groups; create a new  DF from that
        private = self.private_messaging_analyzer.filter(channels=name).stats.df
        group = self.group_messaging_analyzer.filter(senders=name)
        groups = [
            self.group_messaging_analyzer.filter(channels=g).stats.df for g in group
        ]
        df = utils.stack_dfs(private, *groups)
        return ConversationStats(df)


class MessagingAnalyzer:
    def __init__(self, data: Dict[str, Conversation], kind) -> None:
        self.data = data  # channel to convo map
        self.kind = kind
        self.df: pd.DataFrame = self.get_df(self.data)

        self._stats = ConversationStats(self.df)
        # TODO maybe rename
        self.group_convo_map = utils.get_group_convo_map(data)  # name to convo map

        self._stats_per_channel = self.get_stats_per_channel()
        self._stats_per_sender = self.get_stats_per_sender()

    @property
    def is_group(self) -> bool:
        return self.kind == "group"

    @property
    def stats(self) -> ConversationStats:
        return self._stats

    @property
    def stats_per_channel(self) -> Dict[str, ConversationStats]:
        return self.get_stats_per_channel()

    @property
    def stats_per_sender(self) -> Dict[str, ConversationStats]:
        return self.get_stats_per_sender()

    @property
    def participants(self) -> List[str]:
        # super set of self.stats.contributors
        participants = []
        for _, convo in self.data.items():
            participants += convo.metadata.participants
        return sorted(list(set(participants)))

    @property
    def portion_of_contribution(self) -> Dict[str, float]:
        ranking_dict = self.get_ranking_of_partners_by_convo_stats()
        hundred = sum(list(ranking_dict.values()))
        return {name: value * 100 / hundred for name, value in ranking_dict.items()}

    @property
    def most_contributed(self) -> str:
        return list(self.portion_of_contribution.items())[0]

    @property
    def least_contributed(self) -> str:
        return list(self.portion_of_contribution.items())[-1]

    @property
    def min_group_size(self) -> int:
        sizes = self.get_convos_size(self.data)
        return min(sizes.values())

    @property
    def max_group_size(self) -> int:
        sizes = self.get_convos_size(self.data)
        return max(sizes.values())

    @property
    def mean_group_size(self) -> float:
        sizes = self.get_convos_size(self.data)
        return sum(sizes.values()) / len(sizes.values())

    @property
    def number_of_convos_created_by_me(self) -> int:
        return sum([stat.created_by_me for stat in self.stats_per_channel.values()])

    def get_stats_per_channel(self) -> Dict[str, ConversationStats]:
        return {
            channel: ConversationStats(convo.data)
            for channel, convo in self.data.items()
        }

    def get_stats_per_sender(self) -> Dict[str, ConversationStats]:
        stat_per_participant = {}
        for name in self.participants:
            stat_per_participant[name] = self.stats.filter(sender=name)
        return stat_per_participant

    def get_all_groups_for_one_person(self, name) -> List[str]:
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.stats.filter(**kwargs)
        return getattr(stats, attribute)

    def get_ranking_of_partners_by_convo_stats(self, statistic: str = "mc") -> Dict:
        count_dict = {}
        stats_per_people = (
            self.stats_per_sender if self.is_group else self.stats_per_channel
        )

        if len(stats_per_people) == 1:
            raise utils.TooFewPeopleError("Can't rank one person.")

        for name, stats in stats_per_people.items():
            count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
            count_dict = utils.sort_dict(
                count_dict, func=lambda item: item[1], reverse=True
            )

        return count_dict

    @staticmethod
    def get_df(convos) -> pd.DataFrame:
        return utils.stack_dfs(*[convo.data for convo in convos.values()])

    # TODO myabe move this to a filterer class?!?!?!
    @utils.string_kwarg_to_list_converter("senders")
    @utils.string_kwarg_to_list_converter("channels")
    def filter(self, channels=None, senders=None):
        # TODO test if can pipe filters like this or not by filtering for both channels and senders
        # see how it behaves with private as well
        if senders is None and channels is None:
            return self
        data = copy.copy(self.data)
        if senders is not None:
            data = self.filter_by_sender(data, senders)
        if channels is not None:
            # todo rename filter_by_channel
            data = self.filter_by_channel(data, channels)
        if not data:
            return None
        return MessagingAnalyzer(data, self.is_group)

    @staticmethod
    def filter_by_sender(
        data: Dict[str, Conversation], names: List[str]
    ) -> Dict[str, Conversation]:
        new_data = {}
        for key, g in data.items():
            if list(set(g.metadata.participants) & set(names)):
                new_data[key] = g
        return new_data

    @staticmethod
    def filter_by_channel(
        data: Dict[str, Conversation], groups: List[str]
    ) -> Dict[str, Conversation]:
        try:
            new_data = {name: data[name] for name in groups}
            return new_data
        except KeyError:
            return {}

    @staticmethod
    def get_convos_size(data) -> Dict[str, int]:
        sizes = {}
        for k, g in data.items():
            size = len(g.metadata.participants)
            sizes[k] = size
        return sizes
