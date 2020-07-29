from utils import year_converter, month_converter, year_and_month_checker
from ConversationAnalyzer import ConversationAnalyzer


# TODO
# time series analysis

# later:
# implement and test most used msgs and words
# implement and test most messages/(maybe words and chars) sent a day/hour/(maybe month and year)


class MessagingAnalyzer:
    def __init__(self, names, people): # TODO input people only. class ill know what to do

        self.names = names
        self.people = people

    def get_conversation_stats(self, name):
        analyzer = ConversationAnalyzer(self.people.get(name))
        if analyzer is None:  # TODO this is too explicit ?!
            return None
        return analyzer.get_stats()

    def get_messages(self, name):
        return self.people.get(name).messages

    def get_count(self, year=None, month=None, subject='all', property=None):
        count = 0
        # we have a list of names we want to iterate over
        for name in self.names:
            stats = self.get_conversation_stats(name=name)
            if stats is None:  # TODO too explicit
                continue
            count += self.get_count_for_a_person(stats, year=year, month=month, subject=subject, property=property)
        return count

    @year_and_month_checker
    def get_count_for_a_person(self, stats, year=None, month=None, subject='all', property=None):
        if year is None and month is None:
            # add up all the messages count
            return getattr(stats.get(subject), property)
        elif year and not month:
            # add up all the messages count in that year
            return self.loop_over_months(stats.get('grouped').get(year), subject=subject, property=property)
        elif year and month:
            # add up all the messages count in that year and month
            # TODO get month does not work if year has no messages
            # TODO subject does not work if not year or month in grouped
            # see bank transfers solution: year month checker
            return getattr(stats.get('grouped').get(year).get(month).get(subject), property)


    # 1. Ranking of friends by total count of messages/words/characters (also by year/month)

    def total_number_of_messages(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='all', property='msg_count')

    def total_number_of_words(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='all', property='word_count')

    def total_number_of_characters(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='all', property='char_count')

    # 2. Ranking of friends who I sent the most messages/words/characters (also by year/month)

    def total_number_of_messages_sent(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='me', property='msg_count')

    def total_number_of_words_sent(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='me', property='word_count')

    def total_number_of_characters_sent(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='me', property='char_count')

    # 3. Ranking of friends who sent the most messages/words/characters (also by year/month)

    def total_number_of_messages_received(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='partner', property='msg_count')

    def total_number_of_words_received(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='partner', property='word_count')

    def total_number_of_characters_received(self, year=None, month=None):
        return self.get_count(year=year, month=month, subject='partner', property='char_count')

    # 4. Most used messages/words in convos by me/partner (also by year/month)

    def most_used_messages_by_me(self, year=None, month=None):
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

    def most_used_messages_by_partners(self, year=None, month=None):
        pass

    def most_used_words_by_me(self, year=None, month=None):
        pass

    def most_used_words_by_partners(self, year=None, month=None):
        pass

    # 5. Number of messages sent/got (also by year/month/day/hour)
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

    # 6. Time series: dict of 'year/month/day : number of messages/words/characters (also sent/got) for user/all convos'
    # 7.

    @staticmethod
    def loop_over_months(data, subject='all', property=None):  # TODO generalize
        count = 0
        if not data:
            print('The selected year has no data.')
            return count
        for stats in data.values():  # stats is the statistics for a month
            count += getattr(stats.get(subject), property)
        return count


