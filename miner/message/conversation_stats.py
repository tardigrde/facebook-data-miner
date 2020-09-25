from __future__ import annotations

import logging
import math
from typing import Union, List, Dict, Any

import numpy as np
import pandas as pd
import polyglot
from polyglot.detect import Detector
from polyglot.detect.base import logger as polyglot_logger

from miner.utils import utils, period_manager, command, const

polyglot_logger.setLevel("ERROR")


class ConversationStats:
    """
    Class for calculating and storing information and statistics of messages based on an input `Conversations.data`.
    """

    def __init__(self, df: pd.DataFrame, config: Dict[str, Any]) -> None:
        self._df: pd.DataFrame = df
        self._config = config
        self._stats_df: pd.DataFrame = self._get_convos_in_numbers()
        self._stat_sum = self._stats_df.sum()

    def __repr__(self) -> str:
        return f"ConversationStats for {self.number_of_channels} channels"

    def __len__(self) -> int:
        return len(self.df)

    @property
    def df(self) -> pd.DataFrame:
        """

        @return:
        """
        return self._df

    @property
    def config(self) -> Dict[str, str]:
        """

        @return:
        """
        return self._config

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        """

        @param df:
        @param kwargs:
        @return:
        """
        if df is None:
            df = self.df
        df = self._get_filtered_df(df, **kwargs)
        return ConversationStats(df, self.config)

    def _get_convos_in_numbers(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)

    @property
    def channels(self) -> List[str]:
        """

        @return: all the channels in self.df.
        """
        return list(self.df.partner.unique()) if "partner" in self.df else []

    @property
    def number_of_channels(self) -> int:
        """

        @return: number of channels in self.df.
        """
        return len(self.channels)

    @property
    def contributors(self) -> List[str]:
        """

        @return: all the participants who sent a message in any channels at least once.
        """
        return list(self.df.sender_name.unique()) if "sender_name" in self.df else []

    @property
    def number_of_contributors(self) -> int:
        """

        @return: number of contributors.
        """
        return len(self.contributors)

    @property
    def creator(self) -> str:
        """

        @return: returns the name of the contributor who started the channel.
        """
        if self.number_of_channels < 1:
            return ""
        if self.number_of_channels > 1:
            logging.warning("Too many `channels` to calculate this.")
            # raise utils.TooManyChannelsError("Too many `channels` to calculate this.")
            return ""
        return self.df.iloc[0].sender_name

    @property
    def created_by_me(self) -> bool:
        """

        @return: returns True if the user created the channel, False otherwise.
        """
        return self.creator == self.config.get("profile").name

    @property
    def start(self) -> np.datetime64:
        """

        @return: the timestamp of the first message ever sent in self.df.
        """
        return self.df.index[0] if len(self.df) else None

    @property
    def end(self) -> np.datetime64:
        """

        @return: the timestamp of the last message ever sent in self.df.
        """
        return self.df.index[-1] if len(self.df) else None

    @property
    def messages(self) -> pd.DataFrame:
        """

        @return: returns self.df, that is all the messages in this object.
        """
        return self.df

    @property
    def text(self) -> pd.Series:
        """

        @return: returns only the text messages in this object.
        """
        return (
            self.df[self.df.content.notna()].content.dropna()
            if "content" in self.df
            else pd.Series()
        )

    @property
    def media(self) -> pd.DataFrame:
        """

        @return: returns only the media messages in this object.
        """
        if any([item in self.df.columns for item in const.MEDIA_DIRS]):
            return self.df[self.df.content.isna()][const.MEDIA_DIRS]
        else:
            return pd.DataFrame()

    @property
    def words(self) -> pd.Series:
        """

        @return: returns all the words in all the messages.
        """
        return self._get_words(self.text)

    @property
    def mc(self) -> int:
        """

        @return: count of messages in this object.
        """
        return self._stat_sum.mc

    @property
    def wc(self) -> int:
        """

        @return: count of words in this object.
        """
        return self._stat_sum.wc

    @property
    def cc(self) -> int:
        """

        @return: count of characters in this object.
        """
        return self._stat_sum.cc

    @property
    def text_mc(self) -> int:
        """

        @return: count of text messages in this object.
        """
        return self._stat_sum.text_mc

    @property
    def media_mc(self) -> int:
        """

        @return: count of media messages in this object.
        """
        return self._stat_sum.media_mc

    @property
    def unique_mc(self) -> int:
        """

        @return: unique messages in this object.
        """
        return len(self.text.unique())

    @property
    def unique_wc(self) -> int:
        """

        @return: unique words in all the messages this object.
        """
        return len(set(self.words))

    @property
    def percentage_of_text_messages(self) -> float:
        """

        @return: percentage of text messages compared to all messages.
        """
        return self.text_mc * 100 / self.mc

    @property
    def percentage_of_media_messages(self) -> float:
        """

        @return: percentage of media messages compared to all messages.
        """
        return 100 - self.percentage_of_text_messages

    @property
    def most_used_msgs(self) -> pd.Series:
        """

        @return: most occurring messages in descending order.
        """
        return (
            self.text.value_counts()
            .rename_axis("unique_values")
            .reset_index(name="counts")
        )

    @property
    def most_used_words(self) -> pd.Series:
        """

        @return: most occurring words in descending order.
        """
        return (
            self.words.value_counts()
            .rename_axis("unique_values")
            .reset_index(name="counts")
        )

    @property
    def wc_in_messages(self):
        """

        @return: word count per message.
        """
        wcs = []
        for msg in self.text:
            length = len(msg.split())
            wcs.append(length)
        return wcs

    @property
    def cc_in_messages(self):
        """

        @return: character count per message.
        """
        ccs = []
        for msg in self.text:
            ccs.append(len(msg))
        return ccs

    @property
    def reacted_messages(self) -> pd.Series:
        """

        @return: all the messages with a reaction.
        """
        return (
            self.df[self.df.reactions.notna()]
            if "reactions" in self.df
            else pd.Series()
        )

    @property
    def percentage_of_reacted_messages(self) -> float:
        """

        @return: percentage of reacted messages compared to all messages.
        """
        return len(self.reacted_messages) * 100 / self.__len__()

    @property
    def files(self) -> pd.Series:
        """

        @return: all the messages which are files sent.
        """
        return self.media_message_extractor("files")

    @property
    def photos(self) -> pd.Series:
        """

        @return: all the messages which are photos sent.
        """
        return self.media_message_extractor("photos")

    @property
    def videos(self) -> pd.Series:
        """

        @return: all the messages which are videos sent.
        """
        return self.media_message_extractor("videos")

    @property
    def audios(self) -> pd.Series:
        """

        @return: all the messages which are audio files sent.
        """
        return self.media_message_extractor("audio_files")

    @property
    def gifs(self) -> pd.Series:
        """

        @return: all the messages which are gifs sent.
        """
        return self.media_message_extractor("gifs")

    @property
    def average_word_length(self) -> float:
        """

        @return: average word length.
        """
        lengths = [len(i) for i in self.words]
        return 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths))

    @property
    def message_language_map(self) -> Dict[str, Dict[str, Any]]:
        """

        @return: detected (with polyglot library) language per message.
        """
        map = {}
        for msg in self.text:
            try:
                detect = Detector(msg)
                map[msg] = {
                    "lang": detect.language.name,
                    "confidence": detect.language.confidence,
                }
            except polyglot.detect.base.UnknownLanguage:
                map[msg] = None
        return map

    @property
    def message_language_ratio(
        self,
    ) -> Dict[str, Union[Dict[str, int], Dict[str, float]]]:
        """

         @return: detected (with polyglot library) language ratio.
         """
        count_dict = {}
        for v in self.message_language_map.values():
            if not v:
                utils.fill_dict(count_dict, "Not detected", 1)
                continue
            count_dict = utils.fill_dict(count_dict, v.get("lang"), 1)
        count_dict = utils.sort_dict(
            count_dict, func=lambda item: item[1], reverse=True
        )
        percent_dict = utils.get_percent_dict(count_dict)
        # NOTE top is 100 languages
        count_dict, percent_dict = utils.get_top_N_people(count_dict, percent_dict, 100)

        return {"count": count_dict, "percent": percent_dict}

    def get_grouped_time_series_data(self, timeframe: str = "y") -> pd.DataFrame:
        """

        @param timeframe: in which timeframe you want to group the messages. One of {y|m|d|h}.
        @return: numeric statistics like message, word, char, etc. count grouped by datetime according the timeframe.
        """
        if not len(self._stats_df):
            return pd.DataFrame()
        grouping_rule = period_manager.PERIOD_MANAGER.get_grouping_rules(
            timeframe, self._stats_df
        )
        groups_df = self._stats_df.groupby(grouping_rule).sum()
        return period_manager.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(
            groups_df, timeframe=timeframe
        )

    def stats_per_timeframe(self, timeframe: str, statistic: str = "mc") -> Dict:
        """

        @param timeframe: in which timeframe you want to group the messages. One of {y|m|d|h}.
        @return: numeric statistics like message, word, character, etc. broken down to the timeframe.
        """
        interval_stats = self.get_grouped_time_series_data(timeframe=timeframe)
        return self._count_stat_for_period(
            interval_stats, timeframe, statistic=statistic
        )

    @staticmethod
    def _get_words(messages) -> pd.Series:
        words = []
        if not len(messages):
            return pd.Series(words)
        token_list = messages.str.lower().str.split()
        for tokens in token_list:
            for token in tokens:
                words.append(token)
        return pd.Series(words)

    def _count_stat_for_period(self, df, period, statistic) -> Dict[str, int]:
        # DOES too much
        periods = {}
        if not len(df):
            return periods
        periods = utils.prefill_dict(
            periods,
            utils.get_period_map(self.config.get("profile").registration_timestamp).get(
                period
            ),
            0,
        )

        for date, row in df.iterrows():
            stat = row[statistic]
            if stat is None:
                continue
            key = period_manager.PERIOD_MANAGER.date_to_period(date, period)
            periods = utils.fill_dict(periods, key, stat)
        sorting_func = period_manager.PERIOD_MANAGER.sorting_method(period)
        periods = utils.sort_dict(periods, sorting_func)
        return periods

    def _get_filtered_df(
        self,
        df: pd.DataFrame,
        channels: Union[str, List[str]] = None,
        senders: Union[str, List[str]] = None,
        **kwargs,
    ) -> pd.DataFrame:
        """
        @param df:
        @param channels: Union[str, List[str]] = None,
        @param senders: Union[str, List[str]] = None,
        @param subject: str = "all",
        @param kwargs: {start,end,period} : Union[str, datetime] = None
        @return:
        """
        filter_messages = command.CommandChainCreator()
        filter_messages.register_command(
            utils.filter_by_channel, column="partner", channels=channels
        )
        filter_messages.register_command(
            utils.filter_by_sender,
            column="sender_name",
            senders=senders,
            me=self.config.get("profile").name,
        )
        filter_messages.register_command(utils.filter_by_date, **kwargs)
        filter_messages.register_command(utils.filter_empty_cols)
        return filter_messages(df)


class StatsDataframe:
    def __call__(self, df) -> pd.DataFrame:
        self.df = pd.DataFrame(index=df.index)

        # all message count
        self.df["mc"] = pd.Series([1 for _ in range(len(df))]).values if len(df) else 0

        # text message count
        self.df["text_mc"] = (
            df.content.map(self.calculate_text_mc).values if "content" in df else 0
        )
        # media message count
        self.df["media_mc"] = (
            df.content.map(self.calculate_media_mc).values if "content" in df else 0
        )
        # word count
        self.df["wc"] = (
            df.content.map(self.calculate_wc).values if "content" in df else 0
        )
        # cc
        self.df["cc"] = (
            df.content.map(self.calculate_cc).values if "content" in df else 0
        )
        return self.df

    @staticmethod
    def calculate_text_mc(content: Union[str, math.nan]) -> int:
        return 0 if utils.is_nan(content) else 1

    @staticmethod
    def calculate_media_mc(content: Union[str, math.nan]) -> int:
        return 1 if utils.is_nan(content) else 0

    @staticmethod
    def calculate_wc(content: Union[str, math.nan]) -> int:
        return 0 if utils.is_nan(content) else len(content.split())

    @staticmethod
    def calculate_cc(content: Union[str, math.nan]) -> int:
        return (
            0 if utils.is_nan(content) else sum([len(word) for word in content.split()])
        )
