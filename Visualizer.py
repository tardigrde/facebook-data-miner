import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from People import People
from ConversationAnalyzer import ConversationAnalyzer


# plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})

class Visualizer:
    def __init__(self):
        pass

    def plot_time_series(self, x, y, title="Time series", xlabel='Date', ylabel='Value', dpi=100):
        plt.figure(figsize=(16, 5), dpi=dpi)
        plt.plot(x, y, color='tab:red')
        plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
        plt.show()


def set_up(people, name, interval='y'):
    analyzer = ConversationAnalyzer(name, people.individuals.get(name).messages)
    interval_stats = analyzer.get_time_series_data()
    stats = interval_stats.get(interval)
    return analyzer.get_plotable_time_series_data(stats, statistic='msg_count')


if __name__ == "__main__":
    v = Visualizer()
    TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'
    people = People(path=TEST_DATA_PATH)
    names = ['Teflon Musk', 'Tőke Hal']
    for name in names:
        data = set_up(people, name, interval='d')
        df = pd.DataFrame(data.items(), columns=['date', 'value'])
        v.plot_time_series(x=df.date, y=df.value, title=name)
