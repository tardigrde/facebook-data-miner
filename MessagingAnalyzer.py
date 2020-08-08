from utils import year_converter, month_converter, generate_time_series
from datetime import datetime, date, timedelta
import pandas as pd
from ConversationAnalyzer import ConversationAnalyzer


# TODO
# new column for data, to whom was the message sent? (needed for when we stack up all the dfs)
# time series analysis
#

# later:
# - use dependecy injection?!
# implement and test most used msgs and words
# implement and test most messages/(maybe words and chars) sent a day/hour/(maybe month and year)


class MessagingAnalyzer:
    def __init__(self, names, people):
        # TODO input people only. class ill know what to do
        # NO, USE DEPENDECY INJECTION

        self.names = names
        self.people = people

    def get_count(self, attribute, subject='all', start=None, end=None, period: str = None):
        count = 0
        # we have a list of names we want to iterate over
        for name in self.names:
            stats = self.get_conversation_stats(name=name, subject=subject, start=start, end=end, period=period)
            if stats is not None:  # TODO too explicit; needed because it is possible that None will be returned, if t got an empty df
                count += getattr(stats, attribute)
        return count

    def get_conversation_stats(self, name, subject='all', start=None, end=None, period: str = None):
        messages = self.people.get(name).messages
        analyzer = ConversationAnalyzer(name, messages)
        if analyzer is None:  # TODO this is too explicit ?!
            return None
        return analyzer.get_stats(subject=subject, start=start, end=end, period=period)

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
    """
    TODO:
    - plan:
      - ~~see if filtering the big df works as expected~~
        - ~~filter by date, sender~~
        - ~~output should be another df~~
        - ~~output df is an input for ConvoAnalyzer~~
      - ~~if there is a POC, decide on the data structure~~
      - later nice time-based graph of the above numbers
        - what do I need from global time-series:
          - same as above, but is not implemented
            - how to implement:
              - **should have** ~~OR not have~~ an intermediate data container -> that is a HUGE FUCKING df OR dict with the above data structure, that has the stats

    - implementation:    
      - ~~time series data for one person:~~
        - ~~have all the messages in one df for one person~~
        - ~~date should be the index, first locally,~~ but later change it from the beginning
        - ~~generate y/m/d/h timeseries~~
        - ~~split df to sub-dfs, and generate stats from them right away~~
        - ~~assign stats to  y/m/d/h timeseries entries~~
      - time series data for all people:
        - ~~stack the dfs together~~
        - sort by date
        - ~~generate y/m/d/h timeseries~~
        - split df to sub-dfs, and generate stats from them right away:
          - this would have a problem that ConvoAnalyzer is not general enough. it requires a name, that is only one person.
          - TODO generalize ConvoAnalzyer for this purpose (maybe use `!=`)
        - assign stats to  y/m/d/h timeseries entries
        - somehow incorporate who the message was sent to

    - changes to incorporate:
      1. ~~i want to make the indices the dates of the messages (from the very begining), investigate what would this break~~
      2. ~~i want to remove date column which is used in ConversationAnalyzer. this breaks number 3.~~
      3. ~~i want to omit using multiple dfs for different months sooo `stats.get('grouped')` will be no longer ~~
      4. ~~create a new interface for filtering time on dfs~~

    """

    def stack_all_dfs(self):
        dfs = []
        for name, data in self.people.items():
            df = data.messages
            if df is not None:
                dfs.append(df)
        # TODO do I need to sort by index (date)
        return pd.concat(dfs, ignore_index=True)  # TODO why ignore_index??


# @staticmethod
# def loop_over_months(data, subject='all', attribute=None):  # TODO generalize
#     count = 0
#     if not data:
#         print('The selected year has no data.')
#         return count
#     for stats in data.values():  # stats is the statistics for a month
#         count += getattr(stats.get(subject), attribute)
#     return count

# @staticmethod
# def get_stat_for_intervals(name, df, time_series):
#     data = {}
#     for offset, series in time_series.items():
#         data[offset] = {}
#         for i in range(len(series) - 1):  # only looping len - 1 times
#             start = series[i]
#             end = series[i + 1]  # TODO will we miss the last entry?
#             trimmed = df.loc[start:end]
#
#             # check if it has length
#             data[offset][start] = ConversationAnalyzer(name, trimmed) if len(trimmed.index) else None
#     return data

# @year_and_month_checker
# def get_count_for_a_person(self, stats, year=None, month=None, subject='all', attribute=None):
#     if year is None and month is None:
#         # add up all the messages count
#         return getattr(stats.get(subject), attribute)
#     elif year and not month:
#         # add up all the messages count in that year
#         return None
#         # return self.loop_over_months(stats.get('grouped').get(year), subject=subject, attribute=attribute)
#     elif year and month:
#         # add up all the messages count in that year and month
#         return None
#         # return getattr(stats.get('grouped').get(year).get(month).get(subject), attribute)
# def get_messages(self, name):
#     return self.people.get(name).messages
"""
    TODO:
    - plan:
      - ~~see if filtering the big df works as expected~~
        - ~~filter by date, sender~~
        - ~~output should be another df~~
        - ~~output df is an input for ConvoAnalyzer~~
      - if there is a POC, decide on the data structure
        create one master df
        BUT!!!
        both has a problem of, we loose the information, whom I sent the message (is it even needed)
        - what do I need from user-specific time series:
          - timespan-specific msg/word/char count, down to year/month/day/hour level (basically the stats better filtered, not in a dict)
          - how to implement:
            - one idea would be to have time series lists like: (times = pd.date_range('2012-10-01', periods=289, freq='5min'))
                - [dt(year=2011),2012,2013, ...],
                - [dt(year=2012, month=1), dt(year=2012, month=2), ...],
                - days,
                - hours,
                then we could filter for these timespans, extract the needed lines from the df and save it to another df
                this other df would have stats
                all the dfs for all the timespans would have stats
                that we could plot
                years: 2011: stats, 2012: stats ..... and so ooooooon
          - later nice time-based graph of the above numbers
        - what do I need from global time-series:
          - same as above, but is not implemented
            - how to implement:
              - **should have** ~~OR not have~~ an intermediate data container -> that is a HUGE FUCKING df OR dict with the above data structure, that has the stats

    - implementation:    
      - time series data for one person:
        - ~~have all the messages in one df for one person~~
        - ~~date should be the index, first locally,~~ but later change it from the beginning
        - ~~generate y/m/d/h timeseries~~
        - ~~split df to sub-dfs, and generate stats from them right away~~
        - ~~assign stats to  y/m/d/h timeseries entries~~
      - time series data for all people:
        - ~~stack the dfs together~~
        - sort by date
        - ~~generate y/m/d/h timeseries~~
        - split df to sub-dfs, and generate stats from them right away:
          - this would have a problem that ConvoAnalyzer is not general enough. it requires a name, that is only one person.
          - TODO generalize ConvoAnalzyer for this purpose (maybe use `!=`)
        - assign stats to  y/m/d/h timeseries entries

    - changes to incorportae:
      1. i want to make the indices the dates of the messages (from the very begining), investigate what would this break
      2. i want to remove date column which is used in ConversationAnalyzer. this breaks number 3.
      3. i want to omit using multiple dfs for different months sooo `stats.get('grouped')` will be no longer 

"""

# def hack_around_with_filtering(self, name=None):
#     import datetime
#     if not name:
#         return
#     stats = self.get_conversation_stats(name=name).get('all')
#     df = stats.df
#     print(df.head())
#     df[(df['col1'] >= 1) & (df['col1'] <=1 )]
#     df.query('col1 <= 1 & 1 <= col1')
#     print(df[(df.sender_name == 'Levente Csőke') & (df.date.month == 12)])
#     print(df.date.month)
#     print(df.index)
#     print(df.query('20141101 < date < 20141201'))
#     print()
#     df = df.set_index(['date']).iloc[::-1]
#     print(df.index)
#     print(df)
#     print(df.loc['20141101':'20141201'])
#     print(df.loc[datetime.date(year=2014, month=11, day=1):datetime.date(year=2014, month=12, day=1)])
#     print(df.loc[datetime.datetime(year=2014, month=11, day=10, hour=12, minute=21):datetime.date(year=2014, month=12, day=1)])
#     trimmed_df =df.loc[datetime.datetime(year=2014, month=11, day=10, hour=12, minute=21):datetime.date(year=2014, month=12, day=1)]
#     print(trimmed_df)
#     print(trimmed_df[trimmed_df.sender_name == 'Levente Csőke'])
# 7.


"""
- ~~basic time series would look like this:~~ MAKES NO SENSE. we have the df, use it for filtering and for stats
          - users
          |_ Teflon Musk
            |_ 2010
              |_ january
                |_ 1
                  |_ 0-1
                    |_ message 1 \\ this two
                    |_ message 2 // are in a df
                  |_ 1-2
                  |_ 2-3
                  |_ ...
                |_ 2
                |_ ...
              |_ febr
              |_ ...
            |_ 2011
            |_ 2012
            ...
"""
