import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from miner.People import People
from miner.ConversationAnalyzer import ConversationAnalyzer

# plt.rcParams.update({'figure.figsize': (10, 7), 'figure.dpi': 120})

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


class Visualizer:
    def __init__(self):
        pass

    def plot_convos(self, names):
        people = People(path=TEST_DATA_PATH)
        for name in names:
            data = self.set_up_data(people, name, period='d')
            df = pd.DataFrame(data.items(), columns=['date', 'value'])
            v.plot_time_series(x=df.date, y=df.value, title=name)

    @staticmethod
    def set_up_data(people, name, period='y'):
        analyzer = ConversationAnalyzer(name, people.data.get(name).messages)
        interval_stats = analyzer.get_time_series_data(subject='all', start=None, end=None, period=period)
        return analyzer.get_plottable_time_series_data(interval_stats, statistic='msg_count')

    @staticmethod
    def plot_time_series(x, y, title="Time series", xlabel='Date', ylabel='Value', dpi=100):
        plt.figure(figsize=(16, 5), dpi=dpi)
        plt.plot(x, y, color='tab:red')
        plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
        plt.show()


if __name__ == "__main__":
    names = ['Teflon Musk', 'Tőke Hal']
    v = Visualizer()
    v.plot_convos(names)
