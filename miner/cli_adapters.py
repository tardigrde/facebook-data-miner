from typing import List, Dict

import numpy as np
import pandas as pd

from miner.message.conversation_stats import ConversationStats
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.utils import decorators


class GenericAnalyzerFacade:
    def __init__(self, analyzer):
        self._analyzer = analyzer
        self._private = self._analyzer.private
        self._group = self._analyzer.group
        pass

    def people_i_have_private_convo_with(self) -> List[str]:
        return self._analyzer.people_i_have_private_convo_with

    def people_i_have_group_convo_with(self) -> List[str]:
        return self._analyzer.people_i_have_group_convo_with

    def get_who_i_have_private_convo_with_from_a_group(
        self, group_name: str
    ) -> List[str]:
        return self._analyzer.get_who_i_have_private_convo_with_from_a_group(
            group_name=group_name
        )

    def how_much_i_speak_in_private_with_group_members(
        self, group_name: str
    ) -> Dict[str, int]:
        return self._analyzer.how_much_i_speak_in_private_with_group_members(
            group_name=group_name
        )

    def is_priv_msg_first_then_group(self, name: str) -> bool:
        return self._analyzer.is_private_convo_first_then_group(name=name)


class AnalyzerFacade:
    @decorators.kind_checker
    def __init__(
        self,
        analyzer,
        kind: str = "private",
        channels=None,
        participants=None,
        senders=None,
        **kwargs
    ):
        self.__analyzer = getattr(analyzer, kind).filter(
            channels=channels, participants=participants
        )
        self.__stats = self._analyzer.stats.filter(
            channels=channels, senders=senders, **kwargs
        )

    def __repr__(self) -> str:
        return "AnalyzerFacade"

    @property
    def _analyzer(self) -> MessagingAnalyzerManager:
        return self.__analyzer

    @property
    def _stats(self) -> ConversationStats:
        return self.__stats

    def is_group(self) -> bool:
        return self._analyzer.is_group

    def participant_to_channel_map(self) -> Dict[str, List[str]]:
        return self._analyzer.participant_to_channel_map

    def number_of_convos_created_by_me(self) -> int:
        return self._analyzer.number_of_convos_created_by_me

    def participants(self) -> List[str]:
        return self._analyzer.participants

    def max_channel_size(self) -> int:
        return self._analyzer.max_channel_size

    def mean_channel_size(self) -> int:
        return self._analyzer.mean_channel_size

    def min_channel_size(self) -> int:
        return self._analyzer.min_channel_size

    def all_channels(self, name: str = None) -> List[str]:
        """

        @param name: a partner name.
        @return: all channels for this partner (private and groups).
        """
        if not name:
            return self.channels()
        return self._analyzer.get_all_channels_for_one_person(name)

    def ranking_by_statistic(
        self, by="mc", ranking="percent", top=20
    ) -> Dict[str, float]:
        return self._analyzer.get_ranking_of_people_by_convo_stats(
            statistic=by, top=top
        ).get(ranking)

    ##########################################################################

    def channels(self) -> List[str]:
        return self._stats.channels

    def number_of_channels(self) -> int:
        return self._stats.number_of_channels

    def contributors(self) -> List[str]:
        """
        @return:
        """
        return self._stats.contributors

    def number_of_contributors(self) -> int:
        return self._stats.number_of_contributors

    def creator(self) -> str:
        return self._stats.creator

    def created_by_me(self) -> bool:
        return self._stats.created_by_me

    def start(self) -> np.datetime64:
        return self._stats.start

    def end(self) -> np.datetime64:
        return self._stats.end

    @decorators.outputter
    def messages(self, output: str = None) -> pd.Series:
        return self._stats.messages

    @decorators.outputter
    def text(self, output: str = None) -> pd.Series:
        return self._stats.text

    @decorators.outputter
    def media(self, output: str = None) -> pd.Series:
        return self._stats.media

    @decorators.outputter
    def words(self, output: str = None) -> pd.Series:
        return self._stats.words

    def mc(self) -> int:
        return self._stats.mc

    def wc(self) -> int:
        return self._stats.wc

    def cc(self) -> int:
        return self._stats.cc

    def text_mc(self) -> int:
        return self._stats.text_mc

    def media_mc(self) -> int:
        return self._stats.media_mc

    def unique_mc(self) -> int:
        return self._stats.unique_mc

    def unique_wc(self) -> int:
        return self._stats.unique_wc

    def percentage_of_text_messages(self) -> float:
        return self._stats.percentage_of_text_messages

    def percentage_of_media_messages(self) -> float:
        return self._stats.percentage_of_media_messages

    @decorators.outputter
    def most_used_msgs(self, output: str = None) -> pd.Series:
        return self._stats.most_used_msgs

    @decorators.outputter
    def most_used_words(self, output: str = None) -> pd.Series:
        return self._stats.most_used_words

    @decorators.outputter
    def reacted_messages(self, output: str = None) -> pd.DataFrame:
        return self._stats.reacted_messages

    @decorators.outputter
    def files(self, output: str = None) -> pd.Series:
        return self._stats.files

    @decorators.outputter
    def photos(self, output: str = None) -> pd.Series:
        return self._stats.photos

    @decorators.outputter
    def videos(self, output: str = None) -> pd.Series:
        return self._stats.videos

    @decorators.outputter
    def audios(self, output: str = None) -> pd.Series:
        return self._stats.audios

    @decorators.outputter
    def gifs(self, output: str = None) -> pd.Series:
        return self._stats.gifs

    def average_word_length(self):
        return self._stats.average_word_length

    def message_language_map(self):
        """

        @return:
        """
        return self._stats.message_language_map

    def message_language_ratio(self):
        return self._stats.message_language_ratio

    def portion_of_reacted(self):
        return self._stats.portion_of_reacted

    @decorators.outputter
    def get_grouped_time_series_data(
        self, timeframe: str = "y", output: str = None
    ) -> pd.DataFrame:
        return self._stats.get_grouped_time_series_data(timeframe=timeframe)

    def stats_per_timeframe(self, timeframe: str, statistic: str = "mc") -> Dict:
        return self._stats.stats_per_timeframe(timeframe, statistic=statistic)
