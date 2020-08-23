import os
import time

from miner.message.conversations import Conversations
from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.people import People
from miner.friends import Friends

DATA_PATH = f'{os.getcwd()}/data'


class App:
    """
    Entrypoint. Not yet used extensively.
    # TODO LATER turn it into a cli
    """

    def __init__(self):
        # TODO where to filter
        self._friends = Friends(f'{DATA_PATH}/friends/friends.json')
        self._conversations = Conversations(DATA_PATH)
        self.people = People(friends=self._friends, conversations=self._conversations)

    def analyze_messages(self):
        start = time.time()
        analyzer = ConversationAnalyzer(self._conversations)
        rank = analyzer.get_ranking_of_partners_by_messages(statistic='char_count')
        print('app: ', time.time() - start)


if __name__ == '__main__':
    app = App()
    app.analyze_messages()
