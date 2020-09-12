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
        # TODO maybe move group_convo_map creation to here, not conversations
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
            channels=group_name
        ).participants
        for p in participants:
            if p in self.private_messaging_analyzer.data is not None:
                have.append(p)
        return have

    def how_much_i_speak_in_private_with_group_members(
        self, group_name: str
    ) -> Dict[str, int]:
        person_private_stats_map = {}
        for p in self.get_who_i_have_private_convo_with_from_a_group(group_name):
            person_private_stats_map[p] = self.private_messaging_analyzer.filter(
                channels=p
            ).stats.mc
        return person_private_stats_map

    def all_interactions(
        self, name: str
    ) -> Tuple[ConversationStats, ConversationStats]:
        # NOTE this is only a filterer fnction that can be used
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(senders=name)
        return private, group

    def is_priv_msg_first_then_group(self, name: str) -> bool:
        # TODO test
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(senders=name)
        g_start_times = []
        for g in group.data.keys():
            start_time = self.group_messaging_analyzer.filter(channels=g).stats.start
            g_start_times.append(start_time)

        return any([private.stats.start > group_start for group_start in g_start_times])

    def get_stats_together(self, name: str, subject="all") -> ConversationStats:
        # TODO do we want to get all stats or just the ones they wrote
        # TODO subject can only be all and partner but this is not done yet.... maybe just all
        private, group = self.all_interactions(name=name)
        groups = [
            self.group_messaging_analyzer.filter(channels=g)
            .stats.filter(subject=subject)
            .df
            for g in group.data.keys()
        ]
        df = utils.stack_dfs(private.stats.filter(sender=subject).df, *groups)
        return ConversationStats(df)


class MessagingAnalyzer:  # TODO change kind to is_group=False
    def __init__(self, data: Dict[str, Conversation], kind) -> None:
        self.data = data  # channel to convo map
        self._kind = kind
        self.df: pd.DataFrame = self._get_df(self.data)

        self._stats = ConversationStats(self.df)
        # TODO maybe rename
        self.group_convo_map = utils.get_group_convo_map(data)  # name to convo map

        self._stats_per_channel = self._get_stats_per_channel()
        self._stats_per_sender = self._get_stats_per_sender()

    def __len__(self):
        return len(self.data.keys())

    @property
    def is_group(self) -> bool:
        return self._kind == "group"

    @property
    def stats(self) -> ConversationStats:
        return self._stats

    @property
    def stats_per_channel(self) -> Dict[str, ConversationStats]:
        return self._get_stats_per_channel()

    @property
    def stats_per_sender(self) -> Dict[str, ConversationStats]:
        return self._get_stats_per_sender()

    @property
    def participants(self) -> List[str]:
        # super set of self.stats.contributors
        participants = []
        for _, convo in self.data.items():
            participants += convo.metadata.participants
        return sorted(list(set(participants)))

    @property
    def most_contributed(self) -> str:
        return list(self.get_portion_of_contribution().items())[0]

    @property
    def least_contributed(self) -> str:
        return list(self.get_portion_of_contribution().items())[-1]

    @property
    def min_channel_size(self) -> int:
        sizes = self._get_channels_size(self.data)
        return min(sizes.values())

    @property
    def max_channel_size(self) -> int:
        sizes = self._get_channels_size(self.data)
        return max(sizes.values())

    @property
    def mean_channel_size(self) -> float:
        sizes = self._get_channels_size(self.data)
        return sum(sizes.values()) / len(sizes.values())

    @property
    def number_of_convos_created_by_me(self) -> int:
        return sum([stat.created_by_me for stat in self.stats_per_channel.values()])

    def get_portion_of_contribution(
        self, statistic: str = "mc", top: int = 20
    ) -> Dict[str, float]:
        _, ranking_by_percent = self.get_ranking_of_senders_by_convo_stats(
            statistic=statistic, top=top
        )
        return ranking_by_percent

    def get_all_channels_for_one_person(self, name) -> List[str]:
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.stats.filter(**kwargs)
        return getattr(stats, attribute)

    def get_ranking_of_senders_by_convo_stats(
        self, statistic: str = "mc", top: int = 20
    ) -> Tuple[Dict[str, int], Dict[str, float]]:
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

        hundred = sum(list(count_dict.values()))
        percent_dict = {
            name: value * 100 / hundred for name, value in count_dict.items()
        }

        if top:
            count_dict = {k: count_dict[k] for k in list(count_dict.keys())[:top]}
            percent_dict = {k: percent_dict[k] for k in list(percent_dict.keys())[:top]}

        return count_dict, percent_dict

    # TODO myabe move this to a filterer class?!?!?!
    @utils.string_kwarg_to_list_converter("senders")
    @utils.string_kwarg_to_list_converter("channels")
    def filter(self, channels=None, senders=None):
        # TODO test if can pipe filters like this or not by filtering for both channels and senders
        # see how it behaves with private as well
        if senders is None and channels is None:
            return self
        data = copy.copy(self.data)
        # TODO filter by channels first maybe?
        if senders is not None:
            data = self._filter_by_sender(data, senders)
        if channels is not None:
            # todo rename filter_by_channel
            data = self._filter_by_channel(data, channels)
        if not data:
            return None
        return MessagingAnalyzer(data, self.is_group)

    def _get_stats_per_channel(self) -> Dict[str, ConversationStats]:
        return {
            channel: ConversationStats(convo.data)
            for channel, convo in self.data.items()
        }

    def _get_stats_per_sender(self) -> Dict[str, ConversationStats]:
        stat_per_participant = {}
        for name in self.participants:
            stat_per_participant[name] = self.stats.filter(sender=name)
        return stat_per_participant

    @staticmethod
    def _get_df(convos) -> pd.DataFrame:
        return utils.stack_dfs(*[convo.data for convo in convos.values()])

    @staticmethod
    def _filter_by_sender(
        data: Dict[str, Conversation], names: List[str]
    ) -> Dict[str, Conversation]:
        new_data = {}
        for key, g in data.items():
            if list(set(g.metadata.participants) & set(names)):
                new_data[key] = g
        return new_data

    @staticmethod
    def _filter_by_channel(
        data: Dict[str, Conversation], groups: List[str]
    ) -> Dict[str, Conversation]:
        try:
            new_data = {name: data[name] for name in groups}
            return new_data
        except KeyError:
            return {}

    @staticmethod
    def _get_channels_size(data) -> Dict[str, int]:
        sizes = {}
        for k, g in data.items():
            size = len(g.metadata.participants)
            sizes[k] = size
        return sizes
