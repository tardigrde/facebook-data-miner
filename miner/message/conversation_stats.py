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

    # def __repr__(self) -> str:
    #     return f"Msg count is {self.mc}"

    def get_conversation_statistics(self) -> pd.DataFrame:
        stats = StatsDataframe()
        return stats(self.df)

    @property
    def stat_sum(self) -> pd.Series:
        return self.stats_df.sum()

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
    def words(self) -> pd.Series:
        return self.get_words(self.messages)

    @property
    def mc(self) -> int:
        return self.stat_sum.mc

    @property
    def wc(self) -> int:
        return self.stat_sum.wc

    @property
    def cc(self) -> int:
        return self.stat_sum.cc

    @property
    def text_mc(self) -> int:
        return self.stat_sum.text_mc

    @property
    def media_mc(self) -> int:
        return self.stat_sum.media_mc

    @property
    def unique_mc(self) -> int:
        return len(self.messages.unique())

    @property
    def unique_wc(self) -> int:
        return len(set(self.words))

    @property
    def most_used_msgs(self) -> pd.Series:
        return self.messages.value_counts()

    @property
    def most_used_words(self) -> pd.Series:
        return self.words.value_counts()

    @property
    def percentage_of_media_messages(self) -> float:
        return self.stat_sum.media_mc * 100 / self.stat_sum.mc

    @property
    def media(self) -> pd.Series:
        return self.df[self.df.content == math.nan]

    @property
    def photos(self) -> pd.Series:
        return self.df.photos.dropna()

    @property
    def files(self) -> pd.Series:
        return self.df.files.dropna()

    @property
    def videos(self) -> pd.Series:
        return self.df.videos.dropna()

    @property
    def audios(self) -> pd.Series:
        return self.df.audios.dropna()

    @property
    def gifs(self) -> pd.Series:
        return self.df.gifs.dropna()

    def filter(self, df: pd.DataFrame = None, **kwargs) -> ConversationStats:
        if df is None:
            df = self.df
        df = self.get_filtered_df(df, **kwargs)
        return ConversationStats(df)

    # 4.  Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def get_most_used_messages(self, top: int) -> pd.Series:
        return self.most_used_msgs[top:]

    # 5. Time series: dict of 'y/m/d/h : number of messages/words/characters (also sent/got) for user/all convos'
    def get_grouped_time_series_data(self, period: str) -> pd.DataFrame:
        grouping_rule = utils.PERIOD_MANAGER.get_grouping_rules(period, self.stats_df)
        groups_df = self.stats_df.groupby(grouping_rule).sum()
        return utils.PERIOD_MANAGER.set_df_grouping_indices_to_datetime(
            groups_df, period=period
        )

    # 6. Number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period: str, statistic: str = "mc") -> Dict:
        interval_stats = self.get_grouped_time_series_data(period=period)
        # NOTE this could be in the class
        return utils.count_stat_for_period(interval_stats, period, statistic=statistic)

    # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(
        self, statistic: str = "mc", **kwargs
    ) -> Dict:
        raise NotImplementedError()

    @staticmethod
    def get_words(messages) -> pd.Series:
        token_list = messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            for token in tokens:
                words.append(token)
        return pd.Series(words)


class PrivateConversationStats(ConversationStats):
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)

    # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(
        self, statistic: str = "mc", **kwargs
    ) -> Dict:
        count_dict = {}
        if len(self.names) == 1:  # DIFFERENT
            raise utils.TooFewPeopleError("Can't rank one person.")

        for name in self.names:
            df = self.df[self.df.partner == name]
            stats = self.filter(df=df, **kwargs)

            count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
            count_dict = utils.sort_dict(
                count_dict, func=lambda item: item[1], reverse=True
            )
        return count_dict

    @staticmethod
    def get_filtered_df(
        df: pd.DataFrame,
        names: Union[str, List[str]] = None,
        subject: str = "all",
        **kwargs,
    ) -> pd.DataFrame:
        filter_messages = utils.CommandChainCreator()
        filter_messages.register_command(
            utils.filter_by_names, column="partner", names=names
        )
        filter_messages.register_command(
            utils.filter_for_subject, column="sender_name", subject=subject
        )
        filter_messages.register_command(utils.filter_by_date, **kwargs)
        return filter_messages(df)


# TODO
#  is ot okay to have all the groups in same place?
#  not only that, but you can only postfilter for groups
class GroupConversationStats(ConversationStats):
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__(df)
        self.multi = self.number_of_groups > 1
        print(self.df)

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

    @property
    def portion_of_contribution(self):  # TODO my specific stat

        return self.df.sender_name.value_counts(normalize=True) * 100

    # * sign to methods that need other then messages_df

    """
    So this class has 2 use cases based on what df comes in:
    - one group df,
    - more group df stacked.
    
    features/stats for one group:
    - participants,
    - ratio of participation (text, word, char, media, ... join date?),
    - participant messages only,
    
    features/stats for more group:
    - participants,
    - ratio of participation,
    - participant messages only, 
    
    they are actually the same. no difference between one group and more groups.
    it has to be managed by analyzer
    
    Use case:
      private:
        - stats = analyzer.get_stats(filter kwargs)
        - stats.messages
        - stats.wc
        - stats.stats_per_period
      group:
        - 1:
          - stats = analyzer.get_group_stats(filter kwargs)
          - stats.messages
          - stats.number_of_participants
          - stats.get_contribution
        - 2:        
          - gstats = analyzer.group_stats
          - gstats.get_contribution_per_person() # all time
          - gstats.get_person_participant_in_N_grops
          - gstats.messages
    
    
    """

    # filter_by_conversation
    # filter_by_person
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(
        self, statistic: str = "mc", **kwargs
    ) -> Dict:
        pass

    @staticmethod
    def get_filtered_df(
        df: pd.DataFrame,
        names: Union[str, List[str]] = None,
        subject: str = "all",
        **kwargs,
    ) -> pd.DataFrame:
        filter_messages = utils.CommandChainCreator()
        filter_messages.register_command(
            utils.filter_by_names, column="partner", names=names
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
