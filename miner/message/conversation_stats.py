from __future__ import annotations

import logging
import math
from typing import Union, List, Dict, Any

import numpy as np
import pandas as pd
import polyglot
from polyglot.detect import Detector

from miner.utils import utils, period_manager, command


class ConversationStats:
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df: pd.DataFrame, config: Dict[str, Any]) -> None:
        self.df: pd.DataFrame = df
        self.config = config
        self._stats_df: pd.DataFrame = self._get_convos_in_numbers()
        self._stat_sum = self._stats_df.sum()

    def __repr__(self) -> str:
        return f"ConversationStats for {self.number_of_channels} channels"

    def __len__(self):
        return len(self.df)

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        # TODO this does not work if period = 'y'
        if df is None:
            df = self.df
        df = self._get_filtered_df(df, **kwargs)
        return ConversationStats(df, self.config)

    def _get_convos_in_numbers(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)

    @property
    def channels(self) -> List[str]:
        return list(self.df.partner.unique()) if "partner" in self.df else []

    @property
    def number_of_channels(self) -> int:
        return len(self.channels)

    @property
    def contributors(self) -> List[str]:
        return list(self.df.sender_name.unique()) if "sender_name" in self.df else []

    @property
    def number_of_contributors(self) -> int:
        return len(self.contributors)

    @property
    def creator(self) -> str:
        if self.number_of_channels < 1:
            return ""
        if self.number_of_channels > 1:
            logging.warning("Too many `channels` to calculate this.")
            # raise utils.TooManyChannelsError("Too many `channels` to calculate this.")
            return ""
        return self.df.iloc[0].sender_name

    @property
    def created_by_me(self) -> bool:
        return self.creator == self.config.get("profile").name

    @property
    def start(self) -> np.datetime64:
        return self.df.index[0] if len(self.df) else None

    @property
    def end(self) -> np.datetime64:
        return self.df.index[-1] if len(self.df) else None

    @property
    def messages(self) -> pd.Series:
        # TODO this only gets content not media messages
        return self.df.content.dropna() if "content" in self.df else pd.Series()

    @property
    def text(self) -> pd.Series:
        return (
            self.df[self.df.content.notna()].content.dropna()
            if "content" in self.df
            else pd.Series()
        )

    @property
    def media(self) -> pd.Series:
        # TODO is this OK?
        return (
            self.df[self.df.content.isna()][
                ["photos", "videos", "audio_files", "gifs", "files"]
            ]
            if self.df.get(["photos", "videos", "audio_files", "gifs", "files"])
            else pd.Series()
        )

    @property
    def words(self) -> pd.Series:
        return self._get_words(self.messages)

    @property
    def mc(self) -> int:
        return self._stat_sum.mc

    @property
    def wc(self) -> int:
        return self._stat_sum.wc

    @property
    def cc(self) -> int:
        return self._stat_sum.cc

    @property
    def text_mc(self) -> int:
        return self._stat_sum.text_mc

    @property
    def media_mc(self) -> int:
        return self._stat_sum.media_mc

    @property
    def unique_mc(self) -> int:
        return len(self.messages.unique())

    @property
    def unique_wc(self) -> int:
        return len(set(self.words))

    @property
    def percentage_of_text_messages(self) -> float:
        return self.text_mc * 100 / self.mc

    @property
    def percentage_of_media_messages(self) -> float:
        return 100 - self.percentage_of_text_messages

    @property
    def most_used_msgs(self) -> pd.Series:
        """
        TODO bad format?
        (fb) levente@debian:~/projects/facebook-data-miner$ ./miner/app.py analyzer group  - most_used_msgs
        ,content
        ok,2
        what do you test,2
        test,2
        basic group messages,2
        i start today,1
        blabla,1
        You named the group marathon.,1
        yapp yapp :D,1
        hmmm,1
        we could go but running is free,1
        marathon?,1
        :D,1

        @return:
        """
        return self.messages.value_counts()

    @property
    def most_used_words(self) -> pd.Series:
        return self.words.value_counts()

    @property
    def wc_in_messages(self):
        wcs = []
        for msg in self.messages:
            length = len(msg.split())
            wcs.append(length)
        return wcs

    @property
    def cc_in_messages(self):
        ccs = []
        for msg in self.messages:
            ccs.append(len(msg))
        return ccs

    @property
    def reacted_messages(self) -> pd.Series:
        return (
            self.df[self.df.reactions.notna()]
            if "reactions" in self.df
            else pd.Series()
        )

    @property
    def files(self) -> pd.Series:
        return self.media_message_extractor("files")

    @property
    def photos(self) -> pd.Series:
        return self.media_message_extractor("photos")

    @property
    def videos(self) -> pd.Series:
        return self.media_message_extractor("videos")

    @property
    def audios(self) -> pd.Series:
        return self.media_message_extractor("audio_files")

    @property
    def gifs(self) -> pd.Series:
        return self.media_message_extractor("gifs")

    @property
    def average_word_length(self):
        lengths = [len(i) for i in self.words]
        return 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths))

    @property
    def message_language_map(self):
        map = {}
        for msg in self.messages:
            try:
                map[msg] = Detector(msg)
            except polyglot.detect.base.UnknownLanguage:
                map[msg] = None
        return map

    def media_message_extractor(self, kind: str) -> pd.Series:
        return self.df[kind].dropna() if kind in self.df else pd.Series()

    def get_grouped_time_series_data(self, period: str = "y") -> pd.DataFrame:
        if not len(self._stats_df):
            return pd.DataFrame()
        grouping_rule = period_manager.PERIOD_MANAGER.get_grouping_rules(
            period, self._stats_df
        )
        groups_df = self._stats_df.groupby(grouping_rule).sum()
        return period_manager.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(
            groups_df, period=period
        )

    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        interval_stats = self.get_grouped_time_series_data(period=period)
        return self._count_stat_for_period(interval_stats, period, statistic=statistic)

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

    def _count_stat_for_period(self, df, period, statistic):
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
        # TODO later add this in if needed because this breaks stuff
        #  basically removes the content column and the exception happens at:
        #         self._stats_per_participant = self._get_stats_per_participant()
        #  DataFrame object has no atribute 'content'
        # maybe precheck if there are messages at all?!
        filter_messages.register_command(utils.filer_empty_cols)
        return filter_messages(df)


class StatsDataframe:
    def __call__(self, df) -> pd.DataFrame:
        self.df = pd.DataFrame(index=df.index)

        # all message count
        self.df["mc"] = pd.Series([1 for _ in range(len(df))]).values if len(df) else 0
        # self.df["mc"] =  df.content.map(lambda x:1) if 'content' in df else 0
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
