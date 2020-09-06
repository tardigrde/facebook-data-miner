from __future__ import annotations

from typing import Union, List, Dict, Callable, Any, NamedTuple
import pandas as pd
import numpy as np
import math

from miner import utils


class ConversationStats:
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df: pd.DataFrame = df
        self._stats_df: pd.DataFrame = self.get_convos_in_numbers()
        self._stat_sum = self._stats_df.sum()

    def __repr__(self) -> str:
        return f"Stats for: {self.number_of_channels} channels"

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        if df is None:
            df = self.df
        df = self.get_filtered_df(df, **kwargs)
        return ConversationStats(df)

    def get_convos_in_numbers(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)

    @property
    def channels(self) -> List[str]:
        # todo name it channels: either of Union[private convo partner, group,List[private convo partner], List[group]]
        return list(self.df.partner.unique())

    @property
    def number_of_channels(self) -> int:
        return len(self.channels)

    @property
    def contributors(self) -> List[str]:
        # TODO whay about this?
        #     mask = self.df.sender_name != utils.ME
        #     return self.df.sender_name[mask].unique().tolist()
        return list(self.df.sender_name.unique())

    @property
    def number_of_contributors(self) -> int:
        return len(self.contributors)

    @property
    def creator(self) -> str:
        return self.df.iloc[0].sender_name

    @property
    def created_by_me(self) -> bool:
        return self.creator == utils.ME

    @property
    def start(self) -> np.datetime64:
        return self.df.index[0]

    @property
    def end(self) -> np.datetime64:
        return self.df.index[-1]

    @property
    def messages(self) -> pd.Series:
        return self.df.content.dropna()

    @property
    def text(self) -> pd.Series:
        return self.df[self.df.content != math.nan]

    @property
    def media(self) -> pd.Series:
        return self.df[self.df.content == math.nan]

    @property
    def words(self) -> pd.Series:
        return self.get_words(self.messages)

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
        return self.messages.value_counts()

    @property
    def most_used_words(self) -> pd.Series:
        return self.words.value_counts()

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
        return self.media_message_extractor("audios")

    @property
    def gifs(self) -> pd.Series:
        return self.media_message_extractor("gifs")

    def media_message_extractor(self, kind: str) -> pd.Series:
        if kind not in self.df:
            return pd.Series([])
        return self.df[kind].dropna()

    def get_grouped_time_series_data(self, period: str = "y") -> pd.DataFrame:
        grouping_rule = utils.PERIOD_MANAGER.get_grouping_rules(period, self._stats_df)
        groups_df = self._stats_df.groupby(grouping_rule).sum()
        return utils.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(
            groups_df, period=period
        )

    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        interval_stats = self.get_grouped_time_series_data(period=period)
        return self.count_stat_for_period(interval_stats, period, statistic=statistic)

    @staticmethod
    def get_words(messages) -> pd.Series:
        token_list = messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            for token in tokens:
                words.append(token)
        return pd.Series(words)

    @staticmethod
    def count_stat_for_period(df, period, statistic):
        # DOES too much
        periods = {}
        periods = utils.prefill_dict(periods, utils.PERIOD_MAP.get(period), 0)

        for date, row in df.iterrows():
            stat = row[statistic]
            if stat is None:
                continue
            key = utils.PERIOD_MANAGER.date_to_period(date, period)
            periods = utils.fill_dict(periods, key, stat)
        sorting_func = utils.PERIOD_MANAGER.sorting_method(period)
        periods = utils.sort_dict(periods, sorting_func)
        return periods

    @staticmethod
    def get_filtered_df(
        df: pd.DataFrame,
        channel: Union[str, List[str]] = None,
        sender: Union[str, List[str]] = None,
        subject: str = "all",
        **kwargs,
    ) -> pd.DataFrame:
        """
        @param df:
        @param channel: Union[str, List[str]] = None,
        @param sender: Union[str, List[str]] = None,
        @param subject: str = "all",
        @param kwargs: {start,end,period} : Union[str, datetime] = None
        @return:
        """
        filter_messages = utils.CommandChainCreator()
        filter_messages.register_command(
            utils.filter_by_channel, column="partner", channel=channel
        )
        filter_messages.register_command(
            utils.filter_by_sender, column="sender_name", sender=sender
        )
        filter_messages.register_command(
            utils.filter_for_subject, column="sender_name", subject=subject
        )
        filter_messages.register_command(utils.filter_by_date, **kwargs)
        return filter_messages(df)


class StatsDataframe:
    def __init__(self,) -> None:
        self.df = pd.DataFrame()

    def __call__(self, df) -> pd.DataFrame:
        # all message count
        self.df["mc"] = df.content.map(lambda x: 1)
        # text message count
        self.df["text_mc"] = df.content.map(self.calculate_text_mc)
        # media message count
        self.df["media_mc"] = df.content.map(self.calculate_media_mc)
        # word count
        self.df["wc"] = df.content.map(self.calculate_wc)
        # cc
        self.df["cc"] = df.content.map(self.calculate_cc)
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
