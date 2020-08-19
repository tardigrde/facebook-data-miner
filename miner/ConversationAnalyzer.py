import pandas as pd

from miner.ConversationStats import ConversationStats
from miner import utils


class ConversationAnalyzer:
    """
    Analyzer for analyzing specific and/or all conversations

    """

    def __init__(self, people):
        self.people = people
        self.people_data = people.data
        self.names = list(people.names)
        self.multi = len(self.people_data) > 1

        if self.multi:
            self.df = self.stack_dfs(self.people_data)
        else:
            self.df = self.people_data.get(self.names[0]).messages

    def __str__(self):
        if self.multi:
            return self.names
        else:
            return f'{self.names[0]}: {list(self.df.index)}'

    @property
    def stats(self):
        return self.get_stats()

    def get_stats_for_intervals(self, time_series, period, subject='all'):
        data = {}
        for i in range(len(time_series)):
            start = time_series[i]
            try:  # with this solution we will have data for the very last moments until datetime.now()
                end = time_series[i + 1]
            except IndexError:
                end = None
            data[start] = self.get_stats(df=self.df, subject=subject, start=start, end=end, period=period)
        return data

    def get_stats(self, df=None, subject='all', start=None, end=None, period=None):
        df = self.df if df is None else df
        df = self.filter_by_input(df, subject=subject, start=start, end=end, period=period)
        stats = ConversationStats(df)
        return stats

    # 1. Total count of messages/words/characters (also by year/month/day/hour)
    # 2. Total count of messages/words/characters sent (also by year/month/day/hour)
    # 3. Total count of messages/words/characters received (also by year/month)
    def get_count(self, attribute, subject='all', start=None, end=None, period=None):
        stats = self.get_stats(subject=subject, start=start, end=end, period=period)
        return getattr(stats, attribute)

    # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def most_used_messages_(self, **kwargs):
        """
        >>> s1 = pd.Series([3, 1, 2, 3, 4, 1, 1])
        >>> s2 = pd.Series([3, 2, 1, 1])
        >>> s1_vc = s1.value_counts()
        >>> s2_vc = s2.value_counts()
        TODO LATER most used is already a problem:
          - because its a series of all the unique messages/words ever used in a convo
          - it contains strings like ':d', ':p' and 'xd'
          - from all the convos the result of value_counts has to be cleared
          and has to be truncated (that is not use the 200th most used word, only top10 let's say)
          - then these series has to be merged in a way that the same string's counts are added up
          - what about typos????!
        """
        pass

    # 5. Number of messages sent/got on busiest period (by year/month/day/hour)
    def stat_per_period(self, period, statistic, **kwargs):
        interval_stats = self.get_time_series_data(period, **kwargs)
        time_series_data = self.get_stat_count(interval_stats, statistic=statistic)
        return utils.count_stat_for_period(time_series_data, period)

    # 6. Time series: dict of 'y/m/d/h : number of messages/words/characters (also sent/got) for user/all convos'
    def get_time_series_data(self, period, subject='all', **kwargs):
        time_series = utils.generate_date_series(period=period, **kwargs)
        return self.get_stats_for_intervals(time_series, period, subject=subject)

    # # 7. Ranking of partners by messages by y/m/d/h, by different stats, by sent/got
    def get_ranking_of_partners_by_messages(self, statistic='msg_count', **kwargs):
        count_dict = {}
        for name in self.names:
            df = self.df[self.df.partner == name]
            stats = self.get_stats(df=df, **kwargs)
            if stats is not None:
                count_dict = utils.fill_dict(count_dict, name, getattr(stats, statistic))
        return count_dict

    @staticmethod
    def stack_dfs(people_data):
        dfs = []
        for data in people_data.values():
            if data.messages is not None:
                dfs.append(data.messages)
        return pd.concat(dfs).sort_index()

    @staticmethod
    @utils.attribute_checker
    def get_stat_count(interval_stats, statistic='msg_count'):
        for k, v in interval_stats.items():
            interval_stats[k] = getattr(v, statistic)
        return interval_stats

    @staticmethod
    @utils.subject_checker
    @utils.date_checker
    @utils.start_end_period_checker
    def filter_by_input(df, subject='all', start=None, end=None, period=None):

        if subject == 'me':
            df = df[df.sender_name == 'Levente Csőke']
        elif subject == 'partner':
            df = df[df.sender_name != 'Levente Csőke']
        if start and end:
            df = df.loc[start:end]
        elif start and not end:
            df = df.loc[start:start + period]
        elif not start and end:
            df = df.loc[end - period:end]
        return df
