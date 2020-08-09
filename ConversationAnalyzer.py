import pandas as pd
from utils import date_checker, period_checker, subject_checker, generate_time_series, get_stats_for_intervals


class ConversationAnalyzer:
    def __new__(cls, name, messages, *args, **kwargs):
        if messages is None:  # This deals with the case if no messages
            return None
        return super(ConversationAnalyzer, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name, messages):
        self.name = name
        self.df = messages

    def __str__(self):
        return f'{self.name}: {list(self.df.index)}'

    @property
    def stats(self):
        return self.get_stats(self.df)

    # TODO has to be tested
    def get_time_series_data(self, subject='all', **kwargs):
        time_series = generate_time_series(**kwargs)
        return get_stats_for_intervals(self.get_stats, self.df, time_series, subject=subject)

    def get_plotable_time_series_data(self, interval_stats, statistic):
        for k, v in interval_stats.items():
            if isinstance(v, ConversationStats):
                interval_stats[k] = getattr(v, statistic)
        return interval_stats

    def get_stats(self, df, subject='all', start=None, end=None, period=None):
        df = self.filter_by_input(df, subject=subject, start=start, end=end, period=period)
        stats = ConversationStats(df)
        return stats

    @staticmethod
    @subject_checker
    @date_checker
    @period_checker
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


class ConversationStats:
    """
    Statistics of conversation with one person.
    """

    # TODO do we need this or not?!?! smh
    # def __new__(cls, df, *args, **kwargs):
    #     if not len(df.index):  # This deals with the case if input df is empty
    #         return None
    #     return super(ConversationStats, cls).__new__(cls, *args, **kwargs)

    def __init__(self, df):
        self.df = df

    def __repr__(self):
        return f'{self.msg_count}'

    @property
    def messages(self):
        return self.df.content.dropna()

    @property
    def words(self):
        return self.get_words()

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
        # TODO first few (1-10) messages
        return self.messages.value_counts()

    # 4.
    @property
    def msg_frequency(self):
        # TODO this has been most likely depracated
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
        s = pd.Series(self.words)
        return s.value_counts()

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
    def most_used_chars(self):
        return None  # TODO or not  https://stackoverflow.com/questions/4131123/finding-the-most-frequent-character-in-a-string

    # 11.
    @property
    def rate_of_media_messages(self):
        pass  # TODO what?

    def get_words(self):
        token_list = self.messages.str.lower().str.split()
        words = []
        for tokens in token_list:
            # print(tokens)
            if not isinstance(tokens, list):
                print('WARNING! Not a list!')
                continue  # TODO ??? check this
            for token in tokens:
                words.append(token)
        return words
