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
        self.stats_df: pd.DataFrame = self.get_conversation_statistics()

        self.names = self.df.partner.unique().tolist()

    def __repr__(self) -> str:
        return f'Msg count is {self.msg_count}'

    @property
    def messages(self) -> pd.Series:
        return self.df.content.dropna()

    @property
    def words(self) -> List[str]:
        return self.get_words()

    @property
    def start(self) -> np.datetime64:
        return self.df.index[0]

    @property
    def end(self) -> np.datetime64:
        return self.df.index[-1]

    @property
    def stat_sum(self) -> pd.Series:
        return self.stats_df.sum()

    @property
    def msg_count(self) -> int:
        return len(self.df)

    @property
    def unique_msg_count(self) -> int:
        return len(self.messages.unique())

    @property
    def most_used_msgs(self) -> pd.Series:
        return self.messages.value_counts()

    @property
    def word_count(self) -> int:
        return len(self.words)

    @property
    def unique_word_count(self) -> int:
        return len(set(self.words))

    @property
    def most_used_words(self) -> pd.Series:
        # NOTE this should be pd.Series by default
        return pd.Series(self.words).value_counts()

    @property
    def char_count(self) -> int:
        char_count = 0
        for word in self.words:
            char_count += len(word)
        return char_count

    @property
    def percentage_of_media_messages(self) -> float:
        summa = self.stat_sum
        return summa.media_count * 100 / summa.msg_count

    def get_filtered_stats(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        if df is None:
            df = self.df
        df = self.filter(df, **kwargs)
        return ConversationStats(df)

    # 4.  Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def get_most_used_messages(self, top: int) -> pd.Series:
        return self.most_used_msgs[top:]

    # 5. Time series: dict of 'y/m/d/h : number of messages/words/characters (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period: str) -> pd.DataFrame:
        grouping_rule = utils.PERIOD_MANAGER.get_grouping_rules(period, self.stats_df)
        groups_df = self.stats_df.groupby(grouping_rule).sum()
        return utils.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(groups_df, period=period)

    # 6. Number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period: str, statistic: str = 'msg_count') -> Dict:
        interval_stats = self.get_grouped_time_series_data(period=period)
        # NOTE this could be in the class
        return utils.count_stat_for_period(interval_stats, period, statistic=statistic)

    # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic: str = 'msg_count', **kwargs) -> Dict:
        count_dict = {}
        if len(self.names) == 1:
            raise utils.TooFewPeopleError("Can't rank one person.")

        for name in self.names:
            df = self.df[self.df.partner == name]
            stats = self.get_filtered_stats(df=df, **kwargs)
            count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
            count_dict = utils.sort_dict(count_dict, func=lambda item: item[1], reverse=True)
        return count_dict

    def get_words(self) -> List[str]:
        token_list = self.messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            if not isinstance(tokens, list):
                print('WARNING! Not a list!')
                continue
            for token in tokens:
                words.append(token)
        return words

    def filter(self, df: pd.DataFrame, names: Union[str, List[str]] = None, subject: str = 'all',
               **kwargs) -> pd.DataFrame:
        filter_messages = utils.CommandChainCreator()
        filter_messages.register_command(utils.filter_by_names, column='partner', names=names)
        filter_messages.register_command(utils.filter_for_subject, column='sender_name', subject=subject)
        filter_messages.register_command(utils.filter_by_date, **kwargs)
        return filter_messages(df)

    def get_conversation_statistics(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)


class StatsDataframe:
    def __init__(self, ) -> None:
        self.df = pd.DataFrame()

    def __call__(self, df) -> pd.DataFrame:
        # all message count
        self.df['msg_count'] = df.content.map(lambda x: 1)
        # text message count
        self.df['text_msg_count'] = df.content.map(self.calculate_text_msg_count)
        # media message count
        self.df['media_count'] = df.content.map(self.calculate_media_count)
        # word count
        self.df['word_count'] = df.content.map(self.calculate_word_count)
        # unique word count
        self.df['unique_word_count'] = df.content.map(self.calculate_unique_word_count)
        # char_count
        self.df['char_count'] = df.content.map(self.calculate_char_count)
        return self.df

    @staticmethod
    def calculate_text_msg_count(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        return 1

    @staticmethod
    def calculate_media_count(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 1
        return 0

    @staticmethod
    def calculate_word_count(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        return len(content.split())

    @staticmethod
    def calculate_unique_word_count(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        return len(set(content.split()))

    @staticmethod
    def calculate_char_count(content: Union[str, math.nan]) -> int:
        if utils.check_if_value_is_nan(content):
            return 0
        words = content.split()
        char_count = 0
        for word in words:
            char_count += len(word)
        return char_count
