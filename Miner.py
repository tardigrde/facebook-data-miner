DATA_PATH = '/home/levente/projects/facebook-data-miner/data'

from People import People
from ConversationAnalyzer import ConversationAnalyzer
from MessagingAnalyzer import MessagingAnalyzer


class Miner:
    def __init__(self):
        pass

    @staticmethod
    def analyze_messages():
        p = People(path=DATA_PATH)

        stats = {}

        for name, person in p.individuals.items():
            #assert name == person.name, 'ERRRRRRROR!!!'
            if person.messages is None:
                stats[person.name] = None
                continue
            analyzer = ConversationAnalyzer(person.name, person.messages)
            stats[person.name] = analyzer.stats
            # if stats[person.name].get('message_count').get('me') > 5000:
            #    top[person.name] = stats[person.name]
        example = stats['Dániel Nagy']
        print()

        # print('LEN: ', len(top.keys()))
        # top_all = {name: data.get('message_count').get('all') for name, data in top.items()}
        # analyzer.visualize_stats(top)

    @staticmethod
    def analyze_messaging():
        p = People(path=DATA_PATH)

        msg_analyzer = MessagingAnalyzer(p.names, p.individuals)

        msgs = msg_analyzer.total_number_of_messages()


if __name__ == '__main__':
    m = Miner()
    m.analyze_messages()
