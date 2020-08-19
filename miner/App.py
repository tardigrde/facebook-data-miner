import os

from miner.ConversationAnalyzer import ConversationAnalyzer
from miner.People import People
from miner.Friends import Friends
from miner.Messaging import Messaging

DATA_PATH = f'{os.getcwd()}/data'

import time


class App:
    """
    Entrypoint. Not yet used extensively.
    # TODO LATER turn it into a cli
    """

    def __init__(self):
        self._friends = Friends(f'{DATA_PATH}/friends/friends.json')
        self._conversations = Messaging(DATA_PATH)
        self.people = People(DATA_PATH, friends=self._friends, conversations=self._conversations)

    def analyze_messages(self):
        start = time.time()
        analyzer = ConversationAnalyzer(self.people)
        rank = analyzer.get_ranking_of_partners_by_messages(statistic='char_count')
        print('app: ', time.time() - start)


if __name__ == '__main__':
    app = App()
    app.analyze_messages()
