from __future__ import annotations
import pandas as pd

from miner import utils
from typing import Union, List, Dict, Callable, Any, NamedTuple


# TODO decide on: can this class live?! I think yes.. for now

class ConversationStats:
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df):
        self.df = df
        self.stats_df = self.get_conversation_statistics()

        self.names = self.df.partner.unique()

    def __repr__(self):
        return f'Msg count is {self.msg_count}'

    def get_filtered_stats(self, df=None, **kwargs):
        if df is None:
            df = self.df
        df = self.filter(df, **kwargs)
        return ConversationStats(df)

    @property
    def messages(self):
        return self.df.content.dropna()

    @property
    def words(self):
        return self.get_words()

    def start(self):
        return self.df.index[0]

    def end(self):
        return self.df.index[-1]

    # 1. Total count of messages/words/characters (also by year/month/day/hour)
    # 2. Total count of messages/words/characters sent (also by year/month/day/hour)
    # 3. Total count of messages/words/characters received (also by year/month)
    # 1.
    @property
    def msg_count(self):
        return len(self.df)

    # 2.
    @property
    def unique_msg_count(self):
        return len(self.messages.unique())

    # 3.
    @property
    def most_used_msgs(self):
        return self.messages.value_counts()

    # 4.
    @property
    def msg_frequency(self):
        # NOTE this has been most likely depracated OR?
        pass

    # 5.
    @property
    def word_count(self):
        return len(self.words)

    # 6.
    @property
    def unique_word_count(self):
        return len(set(self.words))

    # 7.
    @property
    def most_used_words(self):
        return pd.Series(self.words).value_counts()

    # 8.
    @property
    def word_frequency(self):
        pass

    # 9.
    @property
    def char_count(self):
        char_count = 0
        for word in self.words:
            char_count += len(word)
        return char_count

    # 10.
    @property
    def rate_of_media_messages(self):
        """
        TODO LATER
        type of message: is it media or normal? also percentage could be a metric
        search for media messages all 5 of them
        rate is only the second or third abstraction
        """
        pass

    # 4.
    def get_most_used_messages(self, top):
        # TODO
        pass

    # 5. Time series: dict of 'y/m/d/h : number of messages/words/characters (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period):
        grouping_rule = utils.PERIOD_MANAGER.get_grouping_rules(period, self.stats_df)
        groups_df = self.stats_df.groupby(grouping_rule).sum()
        return utils.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(groups_df, period=period)

    # 6. Number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period, statistic):
        interval_stats = self.get_grouped_time_series_data(period=period)
        return utils.count_stat_for_period(interval_stats, period, statistic=statistic)

    # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic='msg_count', **kwargs):
        count_dict = {}
        if len(self.names) == 1:
            # TODO define own exception
            raise SystemExit('Can\'t rank one person.')

        for name in self.names:
            df = self.df[self.df.partner == name]
            stats = self.get_filtered_stats(df=df, **kwargs)
            count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
            count_dict = utils.sort_dict(count_dict, func=lambda item: item[1], reverse=True)
        return count_dict

    def get_words(self):
        token_list = self.messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            if not isinstance(tokens, list):
                print('WARNING! Not a list!')
                continue
            for token in tokens:
                words.append(token)
        return words

    def filter(self, df, names: Union[str, List[str]] = None, subject: str = 'all', start=None, end=None, period=None):
        filter_messages = utils.CommandChainCreator()
        filter_messages.register_command(self.filter_by_name, names=names)
        filter_messages.register_command(self.filter_for_subject, subject=subject)
        filter_messages.register_command(utils.filter_by_date, start=start, end=end, period=period)
        return filter_messages(df)

    def get_conversation_statistics(self):
        stats = StatsDataframe()
        return stats(self.df)

    # TODO see if you can gereralize this
    @staticmethod
    def filter_by_name(df, names):
        if not names:
            return df
        if isinstance(names, str):
            names = [names]
        if not isinstance(names, list):
            raise ValueError(f'Parameter `names` should be type of Union[str, List[str]], got{type(names)}')

        partner_matched = df[df.partner.isin(names)]

        return partner_matched

    @staticmethod
    @utils.subject_checker
    def filter_for_subject(df, subject='all'):
        if subject == 'me':
            return df[df.sender_name == utils.ME]
        elif subject == 'partner':
            return df[df.sender_name != utils.ME]
        return df


class StatsDataframe:
    def __init__(self, ):
        self.df = pd.DataFrame()

    def __call__(self, df):
        # all message count
        self.df['msg_count'] = df.content.map(self.calculate_msg_count)
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
    def calculate_msg_count(content):
        return 1

    @staticmethod
    def calculate_text_msg_count(content):
        if utils.check_if_value_is_nan(content):
            return 0
        return 1

    @staticmethod
    def calculate_media_count(content):
        if utils.check_if_value_is_nan(content):
            return 1
        return 0

    @staticmethod
    def calculate_word_count(content):
        if utils.check_if_value_is_nan(content):
            return 0
        return len(content.split())

    @staticmethod
    def calculate_unique_word_count(content):
        if utils.check_if_value_is_nan(content):
            return 0
        return len(set(content.split()))

    @staticmethod
    def calculate_char_count(content):
        if utils.check_if_value_is_nan(content):
            return 0
        words = content.split()
        char_count = 0
        for word in words:
            char_count += len(word)
        return char_count
