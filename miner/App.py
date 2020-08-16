import os

from miner.Analyzer import Analyzer
from miner.People import People

DATA_PATH = f'{os.getcwd()}/data'


class App:
    """
    Entrypoint. Not yet used extensively.
    # TODO LATER turn it into a cli
    """
    def __init__(self):
        pass

    @staticmethod
    def analyze_messages():
        p = People(path=DATA_PATH)

        analyzer = Analyzer(p)
        rank = analyzer.get_ranking_of_partners_by_messages(attribute='char_count')


if __name__ == '__main__':
    app = App()
    app.analyze_messages()
