DATA_PATH = '/home/levente/projects/facebook-data-miner/data'

from People import People
from ConversationAnalyzer import ConversationAnalyzer


class Miner:
    def __init__(self):
        pass

    @staticmethod
    def analyze_messages():
        p = People(path=DATA_PATH)
        p.to_individuals()

        #top = {}
        stats = {}
        #analyzer = None

        for person in p.individuals:
            if person.messages is None:
                stats[person.name] = None
                continue
            analyzer = ConversationAnalyzer(person.name, person.messages)
            stats[person.name] = analyzer.stats
            #if stats[person.name].get('message_count').get('me') > 5000:
            #    top[person.name] = stats[person.name]
        example = stats['Dóra Boldizsár']
        print()

        #print('LEN: ', len(top.keys()))
        #top_all = {name: data.get('message_count').get('all') for name, data in top.items()}
        #analyzer.visualize_stats(top)


if __name__ == '__main__':
    m = Miner()
    m.analyze_messages()
