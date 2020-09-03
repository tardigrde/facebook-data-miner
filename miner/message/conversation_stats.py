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
        self._stats_df: pd.DataFrame = self.get_conversation_statistics()
        self._stat_sum = self._stats_df.sum()

    # def __repr__(self) -> str:
    #     return f"Msg count is {self.mc}"

    @property
    def names(self):
        # NOTE this will only list people who has
        # once contributed to the group message(s)
        mask = self.df.sender_name != utils.ME
        return self.df.sender_name[mask].unique().tolist()

    def get_conversation_statistics(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)

    @property
    def created_by_me(self):
        return self.df.iloc[0].sender_name == utils.ME

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

    # TODO  I dont like these too much
    @property
    def photos(self) -> pd.Series:
        if "photos" not in self.df:
            return 0
        return self.df.photos.dropna()

    @property
    def files(self) -> pd.Series:
        if "files" not in self.df:
            return 0
        return self.df.files.dropna()

    @property
    def videos(self) -> pd.Series:
        if "videos" not in self.df:
            return 0
        return self.df.videos.dropna()

    @property
    def audios(self) -> pd.Series:
        if "audios" not in self.df:
            return 0
        return self.df.audios.dropna()

    @property
    def gifs(self) -> pd.Series:
        if "gifs" not in self.df:
            return 0
        return self.df.gifs.dropna()

    # 4.  Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def get_most_used_messages(self, top: int) -> pd.Series:
        return self.most_used_msgs[top:]

    # 5. Time series: dict of 'y/m/d/h : number of messages/words/characters (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period: str = "y") -> pd.DataFrame:
        grouping_rule = utils.PERIOD_MANAGER.get_grouping_rules(period, self._stats_df)
        groups_df = self._stats_df.groupby(grouping_rule).sum()
        return utils.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(
            groups_df, period=period
        )

    # 6. Number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        interval_stats = self.get_grouped_time_series_data(period=period)
        # NOTE this could be in the class
        return utils.count_stat_for_period(interval_stats, period, statistic=statistic)

    @staticmethod
    def get_words(messages) -> pd.Series:
        token_list = messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            for token in tokens:
                words.append(token)
        return pd.Series(words)

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


class PrivateConversationStats(ConversationStats):
    """
    Statistics of conversation with one or more persons.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        if df is None:
            df = self.df
        df = self.get_filtered_df(df, **kwargs)
        return PrivateConversationStats(df)


class GroupConversationStats(ConversationStats):
    """
    Statistics of conversation with one or more groups.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)
        self.multi = self.number_of_groups > 1

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        if df is None:
            df = self.df
        df = self.get_filtered_df(df, **kwargs)
        return GroupConversationStats(df)

    @property
    def groups(self):
        return self.df.partner.unique()

    @property
    def number_of_groups(self):
        return len(self.groups)

    @property
    def contributors(self):
        return self.df.sender_name.unique()

    @property
    def number_of_contributors(self):
        return len(self.contributors)

    @property
    def creator(self):
        return self.df.iloc[0].sender_name


class StatsDataframe:
    def __init__(self,) -> None:
        self.df = pd.DataFrame()

    def __call__(self, df) -> pd.DataFrame:
        # TODO do we need this? I don't think so. use length
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
        if utils.check_if_value_is_nan(content):
            return 0
        return 1

    @staticmethod
    def calculate_media_mc(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 1
        return 0

    @staticmethod
    def calculate_wc(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        return len(content.split())

    @staticmethod
    def calculate_cc(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        words = content.split()
        cc = 0
        for word in words:
            cc += len(word)
        return cc


# @staticmethod
# def get_filtered_df(
#         df: pd.DataFrame,
#         channel: Union[str, List[str]] = None,  # could be useful when filtering big dfs
#         subject: str = "all",
#         **kwargs,
# ) -> pd.DataFrame:
#     filter_messages = utils.CommandChainCreator()
#     filter_messages.register_command(
#         utils.filter_by_channel, column="partner", channel=channel
#     )
#     filter_messages.register_command(
#         utils.filter_for_subject, column="sender_name", subject=subject
#     )
#     filter_messages.register_command(utils.filter_by_date, **kwargs)
#     return filter_messages(df)
