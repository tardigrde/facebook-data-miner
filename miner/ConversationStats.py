
class ConversationStats:
    """
    Statistics of conversation with one person.
    """

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
        search for media messages all 5 of them
        rate is only the second or third abstraction
        """
        pass

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
