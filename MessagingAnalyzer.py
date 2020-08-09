from utils import year_converter, month_converter, generate_time_series, get_stats_for_intervals
from datetime import datetime, date, timedelta
import pandas as pd
from ConversationAnalyzer import ConversationAnalyzer

"""

"""


class MessagingAnalyzer:
    def __init__(self, names, people):
        # TODO input people only. class ill know what to do
        self.names = names
        self.people = people

    def time_series_analysis_for_all(self, subject=None, **kwargs):
        time_series = generate_time_series(**kwargs)
        stacked_df = self.stack_dfs(self.people)
        interval_stats = get_stats_for_intervals(self.get_stats, stacked_df, time_series, subject=subject)

    def get_stats(self, df, subject='all', start=None, end=None, period=None):
        # TODO
        # here you have to do something with it
        pass

    def get_count(self, attribute, subject='all', start=None, end=None, period=None):
        count = 0
        # we have a list of names we want to iterate over
        for name in self.names:
            stats = self.get_conversation_stats(name=name, subject=subject, start=start, end=end, period=period)
            if stats is not None:  # TODO too explicit; needed because it is possible that None will be returned, if t got an empty df
                count += getattr(stats, attribute)
        return count

    def get_conversation_stats(self, name, subject='all', start=None, end=None, period=None):
        messages = self.people.get(name).messages
        analyzer = ConversationAnalyzer(name, messages)
        if analyzer is None:  # TODO this is too explicit ?!
            return None
        return analyzer.get_stats(messages, subject=subject, start=start, end=end, period=period)

    def total_number_of_(self, attribute, subject='all', **kwargs):
        return self.get_count(attribute=attribute, subject=subject, **kwargs)

    # 1. Ranking of friends by total count of messages/words/characters (also by year/month/day/hour)
    def total_number_of_messages(self, **kwargs):
        return self.total_number_of_(attribute='msg_count', **kwargs)

    def total_number_of_words(self, **kwargs):
        return self.total_number_of_(attribute='word_count', **kwargs)

    def total_number_of_characters(self, **kwargs):
        return self.total_number_of_(attribute='char_count', **kwargs)

    # 2. Ranking of friends who I sent the most messages/words/characters (also by year/month/day/hour)
    def total_number_of_messages_sent(self, **kwargs):
        return self.total_number_of_(attribute='msg_count', subject='me', **kwargs)

    def total_number_of_words_sent(self, **kwargs):
        return self.total_number_of_(attribute='word_count', subject='me', **kwargs)

    def total_number_of_characters_sent(self, **kwargs):
        return self.total_number_of_(attribute='char_count', subject='me', **kwargs)

    # 3. Ranking of friends who sent the most messages/words/characters (also by year/month)
    def total_number_of_messages_received(self, **kwargs):
        return self.total_number_of_(attribute='msg_count', subject='partner', **kwargs)

    def total_number_of_words_received(self, **kwargs):
        return self.total_number_of_(attribute='word_count', subject='partner', **kwargs)

    def total_number_of_characters_received(self, **kwargs):
        return self.total_number_of_(attribute='char_count', subject='partner', **kwargs)

    # 4. Most used messages/words in convos by me/partner (also by year/month/day/hour)
    def most_used_messages_by_me(self, **kwargs):
        """
        >>> s1 = pd.Series([3, 1, 2, 3, 4, 1, 1])
        >>> s2 = pd.Series([3, 2, 1, 1])
        >>> s1_vc = s1.value_counts()
        >>> s2_vc = s2.value_counts()
        TODO (later) most used is already a problem:
          - because its a series of all the unique messages/words ever used in a convo
          - it contains strings like ':d', ':p' and 'xd'
          - from all the convos the result of value_counts has to be cleared
          and has to be truncated (that is not use the 200th most used word, only top10 let's say)
          - then these series has to be merged in a way that the same string's counts are added up
          - what about typos????!
        """
        pass

    def most_used_messages_by_partners(self, **kwargs):
        pass

    def most_used_words_by_me(self, **kwargs):
        pass

    def most_used_words_by_partners(self, **kwargs):
        pass

    # 5. Number of messages sent/got on busiest period (by year/month/day/hour)
    def days_when_most_messages_sent(self):
        # TODO hard algorithmic problem
        pass

    def days_when_most_messages_received(self):
        pass

    def hours_when_most_messages_sent(self):
        # TODO
        # is this referring to the absolute hour most messages sent??
        # like: 2014.07.25. 15h-16h
        # OR
        # the pattern of most messages sent between this and this hours
        # like: 20h-21h
        # ACTUALLY BOTH
        # for years/months/days/hours
        # BUT this comes from the time series analysis
        pass

    def hours_when_most_messages_received(self):
        pass

    # 6. Time series: dict of 'year/month/day/hour : number of messages/words/characters (also sent/got) for user/all convos'
    # TODO

    @staticmethod
    def stack_dfs(people):
        dfs = []
        for data in people.values():
            if data.messages is not None:
                dfs.append(data.messages)
        # TODO do I need to sort by index (date)? yes!
        return pd.concat(dfs).sort_index()  # TODO why ignore_index??
