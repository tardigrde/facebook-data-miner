import pandas as pd


class ConversationAnalyzer:
    def __new__(cls, name, messages, *args, **kwargs):
        if messages is None:  # This deals with the case if no messages
            return None
        return super(ConversationAnalyzer, cls).__new__(cls, *args, **kwargs)

    def __init__(self, name, messages):
        self.name = name
        self.df = messages

        # self.me_df = self.df[self.df.sender_name == 'Levente Csőke']  # TODO remove hardcoded
        # self.partner_df = self.df[self.df.sender_name == self.name]
        # self.partner_df = self.df[self.df.sender_name != 'Levente Csőke']
        # self._monthly = {}

    # TODO
    # def __repr__(self):
    #     pass
    #
    # def __str__(self):
    #     pass

    @property
    def stats(self):
        return self.get_stats()

    # TODO THIS SHOULD BE somehow queryable
    @property
    def monthly(self):
        return self._monthly

    def get_stats(self, start=None, end=None, subject='all'):
        # stats = {
        #     'all': ConversationStats(self.df),
        #     'me': ConversationStats(self.me_df),
        #     'partner': ConversationStats(self.partner_df),
        #     # TODO USE ANOTHER WAY. stats.get_monthly(year=..., month=...)
        #     # instead of having the dfs already cut, we should only just filter the one and only df for a user
        #     # 'grouped': self.get_stats_by_month()
        # }
        df = self.filter_by_input(start=None, end=None, subject='all')
        stats = ConversationStats(df)
        return stats

    # @date_checker # TODO check if start and end a valid date
    # @subject_checker # TODO check if subject in ('all', 'me', 'partner')
    def filter_by_input(self, start=None, end=None, subject='all'):
        if start and end:
            self.df = self.df.loc[start:end]
        elif start and not end:
            self.df = self.df.loc[start:]
        elif not start and end:
            self.df = self.df.loc[:end]
        if subject == 'me':
            self.df = self.df[self.df.sender_name == 'Levente Csőke']
        elif subject == 'partner':
            self.df = self.df[self.df.sender_name != 'Levente Csőke']


class ConversationStats:
    """
    Statistics of conversation with one person.
    """

    def __init__(self, df):
        self.df = df

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
        return None  # TODO or not TODO https://stackoverflow.com/questions/4131123/finding-the-most-frequent-character-in-a-string

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


# def get_stats_by_month(self):
#     grouped = {}
#
#
#     self.group_by_months()
#     for year in self._monthly.keys():
#         if not grouped.get(year):
#             grouped[year] = {}
#         for month in self._monthly.get(year):
#             df = self._monthly.get(year).get(month)
#             me_df = df[df.sender_name == 'Levente Csőke']
#             #partner_df = df[df.sender_name == self.name]  # TODO maybe omit name and use `!=`
#             partner_df = df[df.sender_name != 'Levente Csőke']  # TODO chaneg hardcoded lc
#             if not grouped.get(year).get(month):
#                 grouped.get(year)[month] = {}
#                 grouped.get(year)[month]['all'] = ConversationStats(df)
#                 grouped.get(year)[month]['me'] = ConversationStats(me_df)
#                 grouped.get(year)[month]['partner'] = ConversationStats(partner_df)
#     return grouped
#
# def group_by_months(self):
#     # TODO REPLACE WITH DATE FILTERING!!
#     # I could just simply filter pandas df (where df.date.year == year && df.date.month == month)
#     indices = self.get_indices_at_new_month(self.df)
#     dfs = self.split_df_at_indices(self.df, indices)
#
#     for df in dfs:
#         date = df['date'][0]  # datetime.strptime(df['date'][0], '%Y-%m-%d')
#         if not self._monthly.get(date.year):
#             self._monthly[date.year] = {}
#         self._monthly[date.year][date.month] = df
#
# @staticmethod
# def get_indices_at_new_month(df):
#     indices = []
#     last_month = -1
#
#     for i, date in enumerate(df['date']):
#         # date = datetime.strptime(timestamp, '%Y-%m-%d')
#         if date.month != last_month:
#             indices.append(i)
#             last_month = date.month
#     return indices
#
# @staticmethod
# def split_df_at_indices(df, indices):
#     indices += [len(df)]
#     return [df.iloc[indices[n]:indices[n + 1]].reset_index(drop=True) for n in range(len(indices) - 1)]

'''
        # me_wc, me_unique_wc = self.word_count(self.me_df)
        # p_wc, p_unique_wc = self.word_count(self.partner_df)
        #
        # me_cc = self.character_count(self.me_df)
        # p_cc = self.character_count(self.partner_df)
        #
        # return {
        #     'message_count': {
        #         'me': len(self.me_df),
        #         'partner': len(self.partner_df),
        #         'all': len(self.me_df) + len(self.partner_df),
        #     },
        #     'word_count': {
        #         'me': me_wc,
        #         'partner': p_wc,
        #         'all': me_wc + p_wc,
        #     },
        #     'character_count': {
        #         'me': me_cc,
        #         'partner': p_cc,
        #         'all': me_cc + p_cc,
        #     },
        # }

    # def get_stat_for(self,df):
    #    return ConversationStats(df)

    # def visualize_stats(self, stats):
    #     print(stats)
    #     # print(sorted(stats.items(), key=operator.itemgetter(1), reverse=True))
    #     stats_sorted = self.sort_stats(stats)
    #     for name, stat in stats_sorted.items():
    #         print(f'{name}:\n {stat}\n')
    #
    # @staticmethod
    # def sort_stats(stats):
    #     stats_sorted = {}
    #     name_wc = {}
    #
    #     for name, stat in stats.items():
    #         name_wc[name] = stat.get('word_count').get('all')
    #     sorted_wc = dict(sorted(name_wc.items(), key=operator.itemgetter(1), reverse=True))
    #
    #     for name, wc in sorted_wc.items():
    #         stats_sorted[name] = stats[name]
    #
    #     return stats_sorted
        # self.tokens = None  # TODO

    # def messages_count(self):
    #     me = len(self.me_df)
    #     partner = len(self.partner_df)
    #     return me, partner
    #
    # @staticmethod
    # def get_words(df):
    #     token_list = df.content.str.lower().str.split()
    #     words = []
    #     for tokens in token_list:
    #         # print(tokens)
    #         if not isinstance(tokens, list):
    #             print('WARNING! Not a list!')
    #             continue  # TODO ??? check this
    #         for token in tokens:
    #             words.append(token)
    #     return words
    #
    # def word_count(self, df):
    #     words = self.get_words(df)
    #     return len(words), len(set(words))

    # def character_count(self, df):
    #     words = self.get_words(df)
    #     char_count = 0
    #
    #     for word in words:
    #         char_count += len(word)
    #     return char_count
    @property
    def words_me(self):
        return self.get_words(self.me_df)

    @property
    def words_partner(self):
        return self.get_words(self.partner_df)
    def unique_word_count(self, party=None):
        if not party:
            return self.stats.get('')


    def most_used_words(self):
        pass

    def number_of_messages_sent(self):
        pass

    def number_of_messages_sent_by_party(self):
        pass

    def number_of_messages_sent_by_time_interval(self):
        pass

    def word_count_per_message(self):
        pass

    def character_count_per_message(self):
        pass
'''
'''
        # messages = 0
        # # we have a dict of `name<string> : person <obj>`
        # # we want to iterate over the dict
        # for name in self.names:
        #     # person = self.people.get(name)
        #     stats = self.get_conversation_stats(name=name)
        #     # if not year and not month
        #     if not year and not month:
        #         # add up all the messages count
        #         messages += stats.get('all').msg_count
        #     # if year and not month
        #     elif year and not month:
        #         def get_msg_count(stat):
        #             return stat.msg_count
        #
        #         # add up all the messages count in that year
        #         messages += self.loop_over_months(stats.get(year), func=get_msg_count)
        #
        #     # if year and month
        #     elif year and month:
        #         # add up all the messages count in that year and month
        #         messages += stats.get(year).get(month)
        # def get_msg_count(stat):
        #     return stat.msg_count
'''
