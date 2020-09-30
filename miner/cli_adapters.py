from typing import Any, Dict, List, Union

import numpy as np
import pandas as pd

from miner.message.conversation_stats import ConversationStats
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.utils import decorators


class MessagingAnalyzerManagerFacade:
    def __init__(self, analyzer: MessagingAnalyzerManager) -> None:
        self._analyzer = analyzer
        self._private = self._analyzer.private
        self._group = self._analyzer.group

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


class MessagingAnalyzerFacade:
    @decorators.kind_checker
    def __init__(
        self,
        analyzer: MessagingAnalyzerManager,
        kind: str = "private",
        channels: Union[str, None] = None,
        participants: Union[str, None] = None,
        senders: Union[str, None] = None,
        **kwargs: Any,
    ) -> None:
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
        """

        @return: ConversationStats object containing stats
        on the current self.df.
        """
        return self.__stats

    def is_group(self) -> bool:
        """

        @return: returns True if we are analyzing group messages,
        False otherwise.
        """
        return self._analyzer.is_group

    def participants(self) -> List[str]:
        """

        @return: list of participants in self.data.
        """
        return self._analyzer.participants

    def participant_to_channel_map(self) -> Dict[str, List[str]]:
        """
        More useful for groups.

        @return: map for every participant to any channels they are in.
        """
        return self._analyzer.participant_to_channel_map

    def number_of_convos_created_by_me(self) -> int:
        """

        @return: number of conversations started by the user.
        """
        return self._analyzer.number_of_convos_created_by_me

    def min_channel_size(self) -> int:
        """
        Makes more sense for groups.

        @return: smallest group size.
        """
        return self._analyzer.min_channel_size

    def max_channel_size(self) -> int:
        """
        Makes more sense for groups.

        @return: largest group size.
        """
        return self._analyzer.max_channel_size

    def mean_channel_size(self) -> float:
        """
        Makes more sense for groups.

        @return: mean group size.
        """
        return self._analyzer.mean_channel_size

    def all_channels(self, name: Union[str, None] = None) -> List[str]:
        """

        @param name: name of the subject we are interested in.
        Anyone who is a participant in at least one conversation.
        @return: all the channels (max 1 private, and any number of
        group conversations) the subject is in.
        """
        if not name:
            return self.channels()
        return self._analyzer.get_all_channels_for_one_person(name)

    def ranking_by_statistic(
        self, by: str = "mc", ranking: str = "percent", top: int = 20
    ) -> Dict[str, float]:
        """

        @param by: attribute we are interested in.
        Can be any of the ConversationStats properties,
        but it has to be numeric.
        @param ranking: format of return value. Any of percent or absolute.
        @param top: used to limit the number of results for better readability.
        @return: dictionary containing ranking in any of percent
        or absolute values.
        """
        return self._analyzer.get_ranking_of_people_by_convo_stats(
            statistic=by, top=top
        ).get(ranking)

    ##########################################################################

    def channels(self) -> List[str]:
        """

        @return: all the channels in self.df.
        """
        return self._stats.channels

    def number_of_channels(self) -> int:
        """

        @return: number of channels in self.df.
        """
        return self._stats.number_of_channels

    def contributors(self) -> List[str]:
        """

        @return: all the participants who sent a message in any channels
        at least once.
        """
        return self._stats.contributors

    def number_of_contributors(self) -> int:
        """

        @return: number of contributors.
        """
        return self._stats.number_of_contributors

    def creator(self) -> str:
        """

        @return: returns the name of the contributor who started the channel.
        """
        return self._stats.creator

    def created_by_me(self) -> bool:
        """

        @return: returns True if the user created the channel, False otherwise.
        """
        return self._stats.created_by_me

    def start(self) -> np.datetime64:
        """

        @return: the timestamp of the first message ever sent in self.df.
        """
        return self._stats.start

    def end(self) -> np.datetime64:
        """

        @return: the timestamp of the last message ever sent in self.df.
        """
        return self._stats.end

    @decorators.outputter
    def messages(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: returns self.df, that is all the messages in this object.
        """
        return self._stats.messages

    @decorators.outputter
    def text(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: returns only the text messages in this object.
        """
        return self._stats.text

    @decorators.outputter
    def media(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: returns only the media messages in this object.
        """
        return self._stats.media

    @decorators.outputter
    def words(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: returns all the words in all the messages.
        """
        return self._stats.words

    def mc(self) -> int:
        """

        @return: count of messages in this object.
        """
        return self._stats.mc

    def wc(self) -> int:
        """

        @return: count of words in this object.
        """
        return self._stats.wc

    def cc(self) -> int:
        """

        @return: count of characters in this object.
        """
        return self._stats.cc

    def text_mc(self) -> int:
        """

        @return: count of text messages in this object.
        """
        return self._stats.text_mc

    def media_mc(self) -> int:
        """

        @return: count of media messages in this object.
        """
        return self._stats.media_mc

    def unique_mc(self) -> int:
        """

        @return: unique messages in this object.
        """
        return self._stats.unique_mc

    def unique_wc(self) -> int:
        """

        @return: unique words in all the messages this object.
        """
        return self._stats.unique_wc

    def percentage_of_text_messages(self) -> float:
        """

        @return: percentage of text messages compared to all messages.
        """
        return self._stats.percentage_of_text_messages

    def percentage_of_media_messages(self) -> float:
        """

        @return: percentage of media messages compared to all messages.
        """
        return self._stats.percentage_of_media_messages

    @decorators.outputter
    def most_used_msgs(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: most occurring messages in descending order.
        """
        return self._stats.most_used_msgs

    @decorators.outputter
    def most_used_words(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: most occurring words in descending order.
        """
        return self._stats.most_used_words

    @decorators.outputter
    def reacted_messages(
        self, output: Union[str, None] = None
    ) -> pd.DataFrame:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages with a reaction.
        """
        return self._stats.reacted_messages

    @property
    def percentage_of_reacted_messages(self) -> float:
        """

        @return: percentage of reacted messages compared to all messages.
        """
        return self._stats.percentage_of_reacted_messages

    @decorators.outputter
    def files(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages which are files sent.
        """
        return self._stats.files

    @decorators.outputter
    def photos(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages which are photos sent.
        """
        return self._stats.photos

    @decorators.outputter
    def videos(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages which are videos sent.
        """
        return self._stats.videos

    @decorators.outputter
    def audios(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages which are audio files sent.
        """
        return self._stats.audios

    @decorators.outputter
    def gifs(self, output: Union[str, None] = None) -> pd.Series:
        """

        @param output: where do we want to write the return value,
        can be any of: {csv|json|/some/path.{json|csv}}.
        @return: all the messages which are gifs sent.
        """
        return self._stats.gifs

    def average_word_length(self) -> float:
        """

        @return: average word length.
        """
        return self._stats.average_word_length

    def message_language_map(self) -> Dict[str, Dict[str, Any]]:
        """

        @return: detected (with polyglot library) language per message.
        """
        return self._stats.message_language_map

    def message_language_ratio(
        self,
    ) -> Dict[str, Union[Dict[str, int], Dict[str, float]]]:
        """

        @return: detected (with polyglot library) language ratio.
        """
        return self._stats.message_language_ratio

    @decorators.outputter
    def get_grouped_time_series_data(
        self, timeframe: str = "y", output: Union[str, None] = None
    ) -> pd.DataFrame:
        """

        @return: numeric statistics like message, word, char, etc.
        count grouped by datetime according the timeframes.
        @param output: where do we want to write the return value, c
        an be any of: {csv|json|/some/path.{json|csv}}.
        @return: numeric statistics like message, word, character, etc.
        count grouped by timeframe.
        """
        return self._stats.get_grouped_time_series_data(timeframe=timeframe)

    def stats_per_timeframe(
        self, timeframe: str, statistic: str = "mc"
    ) -> Dict:
        """

        @param timeframe: in which timeframe you want to group the messages.
        One of {y|m|d|h}.
        @return: numeric statistics like message, word, character, etc.
        broken down to the timeframe.
        """
        return self._stats.stats_per_timeframe(timeframe, statistic=statistic)
