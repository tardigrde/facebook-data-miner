from __future__ import annotations

import copy
from typing import List, Dict, Tuple, Any, Union

import pandas as pd

from miner.message.conversation import Conversation
from miner.message.conversation_stats import ConversationStats
from miner.message.conversations import Conversations
from miner.utils import utils, decorators, command


class MessagingAnalyzerManager:
    def __init__(self, conversations: Conversations, config: Dict[str, Any]) -> None:
        self.conversations = conversations
        self.config = config
        self.private_messaging_analyzer = MessagingAnalyzer(
            conversations.private, config, "private"
        )
        # TODO maybe move group_convo_map creation to here, not conversations
        self.group_messaging_analyzer = MessagingAnalyzer(
            conversations.group, config, "group"
        )

    @property
    def private(self) -> MessagingAnalyzer:
        return self.private_messaging_analyzer

    @property
    def group(self) -> MessagingAnalyzer:
        return self.group_messaging_analyzer

    @property
    def people_i_have_private_convo_with(self) -> List[str]:
        return list(self.private_messaging_analyzer.data.keys())

    @property
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
        group = self.group_messaging_analyzer.filter(participants=name)
        return private, group

    def is_priv_msg_first_then_group(self, name: str) -> bool:
        # TODO test
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(participants=name)
        if group is None or not len(group):
            return True
        g_start_times = []

        for g in group.data.keys():
            start_time = self.group_messaging_analyzer.filter(channels=g).stats.start
            if not start_time:
                continue
            g_start_times.append(start_time)

        return any([private.stats.start > group_start for group_start in g_start_times])

    def get_stats_together(self, name: str) -> ConversationStats:
        private, group = self.all_interactions(name=name)
        groups = [
            group_stats.filter(senders=name).df
            for group_stats in self.group_messaging_analyzer.stats_per_channel.values()
        ]
        df = utils.stack_dfs(private.stats.filter(senders=name).df, *groups)
        return ConversationStats(df, self.config)


class MessagingAnalyzer:
    def __init__(
        self,
        data: Dict[str, Conversation],
        config: Dict[str, Any],
        kind: str = "private",
    ) -> None:
        self.data = data  # channel to convo map
        self.config = config
        self._kind = kind
        self.df: pd.DataFrame = self._get_df(self.data)

        self._stats = ConversationStats(self.df, config)
        # TODO maybe rename
        self.group_convo_map = utils.get_group_convo_map(data)  # name to convo map
        """
        TODO why I have this much
        TODO also could be a df. groups as indices
        (fb) levente@debian:~/projects/facebook-data-miner$ ./miner/app.py analyzer private - group_convo_map
        Tőke Hal:      ["Tőke Hal"]
        Levente Csőke: ["Benedek Elek", "Tőke Hal", "Foo Bar", "Teflon Musk"]
        Foo Bar:       ["Foo Bar"]
        Teflon Musk:   ["Teflon Musk"]
        Benedek Elek:  ["Benedek Elek"]

        """

        self._stats_per_channel = self._get_stats_per_channel()
        self._stats_per_participant = self._get_stats_per_participant()

    def __repr__(self):
        return f"<{self._kind.capitalize()}-MessagingAnalyzer for {self.__len__()} channels>"

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
    def stats_per_participant(self) -> Dict[str, ConversationStats]:
        return self._get_stats_per_participant()

    @property
    def participants(self) -> List[str]:
        # super set of self.stats.contributors
        participants = []
        for _, convo in self.data.items():
            participants += convo.metadata.participants
        return sorted(list(set(participants)))

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

    def get_all_channels_for_one_person(self, name) -> List[str]:
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def get_stat_count(self, attribute: str = "mc", **kwargs) -> int:
        stats = self.stats.filter(**kwargs)
        return getattr(stats, attribute)

    # TODO rename to contributos or participants
    # TODO have a param what to return : percent or count
    # TODO break this function up into pieces
    def get_ranking_of_senders_by_convo_stats(
        self, statistic: str = "mc", top: int = 20
    ) -> Dict[str, Union[Union[dict, dict], Any]]:
        count_dict = {}
        stats_per_people = (
            self.stats_per_participant if self.is_group else self.stats_per_channel
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

        return {"count": count_dict, "percent": percent_dict}

    @decorators.string_kwarg_to_list_converter("channels")
    @decorators.string_kwarg_to_list_converter("participants")
    def filter(self, channels=None, participants=None):
        if participants is None and channels is None:
            return self
        data = copy.copy(self.data)

        filter_messages = command.CommandChainCreator()
        filter_messages.register_command(self._filter_by_channels, channels=channels)
        # this is useless if this is private messaging analyzer
        filter_messages.register_command(
            self._filter_by_participants, participants=participants,
        )
        data = filter_messages(data)
        return MessagingAnalyzer(data, self.config, self._kind)

    def _get_stats_per_channel(self) -> Dict[str, ConversationStats]:
        return {
            channel: ConversationStats(convo.data, self.config)
            for channel, convo in self.data.items()
        }

    def _get_stats_per_participant(self) -> Dict[str, ConversationStats]:
        stat_per_participant = {}
        for name in self.participants:
            stat_per_participant[name] = self.stats.filter(senders=name)
        return stat_per_participant

    @staticmethod
    def _get_df(convos) -> pd.DataFrame:
        if not convos:
            return pd.DataFrame()
        return utils.stack_dfs(*[convo.data for convo in convos.values()])

    @staticmethod
    def _filter_by_channels(
        data: Dict[str, Conversation], channels: List[str] = None
    ) -> Dict[str, Conversation]:
        # TODO do we need all these conditions
        if not channels or (isinstance(channels, list) and not channels[0]):
            return data
        try:

            new_data = {name: data[name] for name in channels}
            return new_data
        except KeyError:
            return {}

    @staticmethod
    def _filter_by_participants(
        data: Dict[str, Conversation], participants: List[str] = None
    ) -> Dict[str, Conversation]:
        # TODO do we need all these conditions
        if not participants or (isinstance(participants, list) and not participants[0]):
            return data
        new_data = {}
        for key, g in data.items():
            if list(set(g.metadata.participants) & set(participants)):
                new_data[key] = g
        return new_data

    @staticmethod
    def _get_channels_size(data) -> Dict[str, int]:
        sizes = {}
        for k, g in data.items():
            size = len(g.metadata.participants)
            sizes[k] = size
        return sizes
