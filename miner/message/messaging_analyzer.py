from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple, Union

import pandas as pd

from miner.message.conversation import Conversation
from miner.message.conversation_stats import ConversationStats
from miner.message.conversations import Conversations
from miner.utils import command, decorators, utils

pd.set_option("mode.chained_assignment", "raise")


class MessagingAnalyzerManager:
    """
    Class that analyzes both private ang group conversations.
    """

    def __init__(
        self, conversations: Conversations, config: Dict[str, Any]
    ) -> None:
        self.conversations = conversations
        self.config = config
        self.private_messaging_analyzer = MessagingAnalyzer(
            conversations.private, config, "private"
        )
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
        return list(
            self.group_messaging_analyzer.participant_to_channel_map.keys()
        )

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
        for p in self.get_who_i_have_private_convo_with_from_a_group(
            group_name
        ):
            person_private_stats_map[
                p
            ] = self.private_messaging_analyzer.filter(channels=p).stats.mc
        return person_private_stats_map

    def all_interactions(
        self, name: str
    ) -> Tuple[ConversationStats, ConversationStats]:
        # NOTE this is only a filterer function
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(participants=name)
        return private, group

    def is_private_convo_first_then_group(self, name: str) -> bool:
        private = self.private_messaging_analyzer.filter(channels=name)
        group = self.group_messaging_analyzer.filter(participants=name)

        if group is None or not len(group):
            return True

        group_start_times = []
        for g in group.data.keys():
            start_time = self.group_messaging_analyzer.filter(
                channels=g
            ).stats.start
            if not start_time:
                continue
            group_start_times.append(start_time)

        return any(
            [
                private.stats.start > group_start
                for group_start in group_start_times
            ]
        )

    def get_stats_together(self, name: str) -> ConversationStats:
        stats = self.group_messaging_analyzer.stats_per_channel.values()
        private, group = self.all_interactions(name=name)
        groups = [group_stats.filter(senders=name).df for group_stats in stats]
        df = utils.stack_dfs(private.stats.filter(senders=name).df, *groups)
        return ConversationStats(df, self.config)


class MessagingAnalyzer:
    """
    Class for analyzing data and metadata of conversations.
    """

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

        self._participant_to_channel_map = utils.particip_to_channel_mapping(
            data
        )

        self._stats_per_channel = self._get_stats_per_channel()
        self._stats_per_participant = self._get_stats_per_participant()

    def __repr__(self) -> str:
        return (
            f"<{self._kind.capitalize()}-MessagingAnalyzer "
            f"for {self.__len__()} channels>"
        )

    def __len__(self) -> int:
        return len(self.data.keys())

    @property
    def is_group(self) -> bool:
        """

        @return: returns True if we are analyzing group messages,
        False otherwise.
        """
        return self._kind == "group"

    @property
    def stats(self) -> ConversationStats:
        """

        @return: ConversationStats object containing stats
        on the current self.df.
        """
        return self._stats

    @property
    def stats_per_channel(self) -> Dict[str, ConversationStats]:
        """

        @return: a dict that contains a ConversationStats object
        for every channel in self.data.
        """
        return self._get_stats_per_channel()

    @property
    def stats_per_participant(self) -> Dict[str, ConversationStats]:
        """

        @return: a dict that contains a ConversationStats object
        for every participant in self.data.
        """
        return self._get_stats_per_participant()

    @property
    def participant_to_channel_map(self):
        """
        Makes more sense for groups.

        @return: map for every participant to any channels they are in.
        """
        return self._participant_to_channel_map

    @property
    def participants(self) -> List[str]:
        """

        @return: list of participants in self.data.
        """
        # super set of self.stats.contributors
        participants = []
        for _, convo in self.data.items():
            participants += convo.metadata.participants
        return sorted(list(set(participants)))

    @property
    def number_of_convos_created_by_me(self) -> int:
        """

        @return: number of conversations started by the user.
        """
        return sum(
            [stat.created_by_me for stat in self.stats_per_channel.values()]
        )

    @property
    def min_channel_size(self) -> int:
        """
        Makes more sense for groups.

        @return: smallest group size.
        """
        sizes = self._get_channels_size(self.data)
        return min(sizes.values())

    @property
    def max_channel_size(self) -> int:
        """
        Makes more sense for groups.

        @return: largest group size.
        """
        sizes = self._get_channels_size(self.data)
        return max(sizes.values())

    @property
    def mean_channel_size(self) -> float:
        """
        Makes more sense for groups.

        @return: mean group size.
        """
        sizes = self._get_channels_size(self.data)
        return sum(sizes.values()) / len(sizes.values())

    def get_all_channels_for_one_person(self, name) -> List[str]:
        """

        @param name: name of the subject we are interested in.
        Anyone who is a participant in at least one conversation.
        @return: all the channels (max 1 private,
        and any number of group conversations) the subject is in.
        """
        groups = []
        for k, g in self.data.items():
            if name in g.metadata.participants:
                groups.append(k)
        return list(set(groups))

    def get_stat_count(self, attribute: str = "mc", **kwargs: Any) -> int:
        """

        @param attribute: attribute we are interested in.
        Can be any of the ConversationStats properties.
        @param kwargs: filtering parameters.
        @return: the statistic one queried for.
        """
        stats = self.stats.filter(**kwargs)
        return getattr(stats, attribute)

    def get_ranking_of_people_by_convo_stats(
        self, statistic: str = "mc", top: int = 20
    ) -> Dict[str, Union[Dict[str, int], Dict[str, float]]]:
        """

        @param statistic: attribute we are interested in.
        Can be any of the ConversationStats properties,
        but it has to be numeric.
        @param top: used to limit the number of results for better readability.
        @return: dictionary containing ranking
        both in percent and absolute values.
        """

        stats_per_people = self._get_stats_per_people()

        if len(stats_per_people) == 1:
            raise utils.TooFewPeopleError("Can't rank one person.")

        count_dict = utils.get_count_dict(stats_per_people, statistic)
        percent_dict = utils.get_percent_dict(count_dict)

        if top:
            count_dict, percent_dict = utils.get_top_N_people(
                count_dict, percent_dict, top
            )

        return {"count": count_dict, "percent": percent_dict}

    @decorators.string_kwarg_to_list_converter("channels")
    @decorators.string_kwarg_to_list_converter("participants")
    def filter(self, channels=None, participants=None):
        """

        @param channels:
        @param participants:
        @return:
        """
        if participants is None and channels is None:
            return self
        data = copy.copy(self.data)

        filter_messages = command.CommandChainCreator()
        filter_messages.register_command(
            self._filter_by_channels, channels=channels
        )
        # this is useless if this is private messaging analyzer
        filter_messages.register_command(
            self._filter_by_participants, participants=participants,
        )
        data = filter_messages(data)
        return MessagingAnalyzer(data, self.config, self._kind)

    def _get_stats_per_people(self):
        stats_per_people = (
            self.stats_per_participant
            if self.is_group
            else self.stats_per_channel
        )
        return stats_per_people

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
        if not channels:
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
        if not participants:
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
