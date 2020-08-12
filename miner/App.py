from miner.ConversationAnalyzer import ConversationAnalyzer
from miner.MessagingAnalyzer import MessagingAnalyzer
from miner.People import People

DATA_PATH = '/home/levente/projects/facebook-data-miner/data'


class App:
    def __init__(self):
        pass

    @staticmethod
    def analyze_messages():
        p = People(path=DATA_PATH)

        stats = {}

        for name, person in p.data.items():
            if person.messages is None:
                stats[person.name] = None
                continue
            analyzer = ConversationAnalyzer(person.name, person.messages)
            stats[person.name] = analyzer.stats
            # if stats[person.name].get('message_count').get('me') > 5000:
            #    top[person.name] = stats[person.name]
        print()

        # print('LEN: ', len(top.keys()))
        # top_all = {name: data.get('message_count').get('all') for name, data in top.items()}
        # analyzer.visualize_stats(top)

    @staticmethod
    def analyze_messaging():
        people = People(path=DATA_PATH)
        msg_analyzer = MessagingAnalyzer(people)


if __name__ == '__main__':
    app = App()
    app.analyze_messages()
