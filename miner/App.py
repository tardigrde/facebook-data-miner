from miner.Analyzer import Analyzer

from miner.People import People

DATA_PATH = '/home/levente/projects/facebook-data-miner/data'


class App:
    def __init__(self):
        pass

    @staticmethod
    def analyze_messages():
        p = People(path=DATA_PATH)

        analyzer = Analyzer(p)
        rank = analyzer.get_ranking_of_friends_by_messages(attribute='char_count')


if __name__ == '__main__':
    app = App()
    app.analyze_messages()
