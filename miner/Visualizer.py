import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

from miner.People import People
from miner.ConversationAnalyzer import ConversationAnalyzer
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/tests/test_data'


# TEST_DATA_PATH = f'{os.getcwd()}/data'


class Visualizer:
    def __init__(self):
        pass

    @staticmethod
    def set_up_data(people, period, stat='msg_count', **kwargs):
        analyzer = ConversationAnalyzer(people)
        interval_stats = analyzer.get_time_series_data(period, **kwargs)
        return analyzer.get_stat_count(interval_stats, statistic=stat)

    def setup_data_for_all_subjects(self, people, period, stat=None, **kwargs):
        all_data = self.set_up_data(people, period, stat=stat, subject='all', **kwargs)
        me_data = self.set_up_data(people, period, stat=stat, subject='me', **kwargs)
        partner_data = self.set_up_data(people, period, stat=stat, subject='partner', **kwargs)
        return all_data, me_data, partner_data

    def plot_time_series_data_of_messages(self, period, name=None, stat='msg_count', **kwargs):
        people = People(path=TEST_DATA_PATH, name=name)
        all_data, me_data, partner_data = self.setup_data_for_all_subjects(people, period, stat, **kwargs)
        d = {
            'date': list(all_data.keys()),
            'all': list(all_data.values()),
            'me': list(me_data.values()),
            'partner': list(partner_data.values())
        }
        df = pd.DataFrame(d).set_index('date')
        self.plot_time_series(df, title=name, stat=stat)

    @staticmethod
    def plot_time_series(df, title="Time series analysis", xlabel='Date', stat='msg_count'):
        ylabel = f'Stat for {stat}'
        df.plot(kind='line', linestyle='dashdot', figsize=(16, 5))
        plt.gca().set(xlabel=xlabel, ylabel=ylabel)
        plt.title(title)  # does not work
        plt.legend()
        plt.show()

    def bar_plot_stat_per_time_period(self, period, name=None, stat='msg_count', **kwargs):
        people = People(path=TEST_DATA_PATH, name=name)
        analyzer = ConversationAnalyzer(people)
        me_stat = analyzer.stat_per_period(period, statistic=stat, subject='me', **kwargs)
        partner_stat = analyzer.stat_per_period(period, statistic=stat, subject='partner', **kwargs)
        d = {
            'date': list(me_stat.keys()),
            'me': list(me_stat.values()),
            'partner': list(partner_stat.values())
        }
        df = pd.DataFrame(d).set_index('date')
        self.plot_stat_per_time(df, stat=stat)

    @staticmethod
    def plot_stat_per_time(df, stat='msg_count', title="Stat per timeperiod", xlabel='Timeperiod', dpi=100):
        # Stacked bar chart
        width = 0.35
        ylabel = f'Stat for {stat}'
        plt.figure(figsize=(12, 12), dpi=dpi)
        plt.bar(list(df.index), list(df.me), width, label='me', color='r')
        plt.bar(list(df.index), list(df.partner), width, label='partner', bottom=list(df.me), color='g')
        plt.gca().set(xlabel=xlabel, ylabel=ylabel)
        plt.title(title)  # does not work
        plt.legend()
        plt.show()

    def plot_ranking_of_friends_by_message_stats(self, stat='msg_count'):
        p = People(path=TEST_DATA_PATH, name='Foo Bar')
        analyzer = ConversationAnalyzer(p)
        ranks_dict = analyzer.get_ranking_of_partners_by_messages(attribute=stat)
        # TODO filteration not with dicts
        # NOTE maybe this could be done by pandas, but maybe we will use these functions elsewhere
        sorted_dict = utils.sort_dict(ranks_dict, func=lambda item: item[1], reverse=True)
        sliced_dict = utils.slice_dict(sorted_dict, 20) if len(sorted_dict) > 20 else sorted_dict
        cleared_dict = utils.remove_items_where_value_is_falsible(sliced_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        self.horizontal_bar_chart(df, stat=stat)

    @staticmethod
    def horizontal_bar_chart(df, stat='msg_count', title='Ranking of friends {}', dpi=100):
        people = list(df.columns)
        y_pos = np.arange(len(people))
        performance = df.iloc[0]

        plt.figure(figsize=(12, 12), dpi=dpi)
        plt.barh(y_pos, performance, align='center', tick_label=people)
        plt.gca().invert_yaxis()  # labels read top-to-bottom
        plt.title(title.format(stat))
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize chat statistics')
    parser.add_argument(
        '-p', '--period', metavar='period', type=str, default='y',
        help='One of {y|m|d|h}, standing for yearly, monthly, daily and hourly breakdown of statisctics.')
    parser.add_argument(
        '-n', '--name', metavar='name', type=str, default=None,
        help="A person's name if you only want data filtered only for them.")
    parser.add_argument(
        '-s', '--stat', metavar='stat', type=str, default='msg',
        help="One of {msg|word|char}, indicating which statistics do you want to get.")

    # TODO add possibility for adding dates from teh command line
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
    args = parser.parse_args()
    period = args.period
    name = args.name
    stat = args.stat
    v = Visualizer()
    v.plot_time_series_data_of_messages(period, name=None, stat=f'{stat}_count')
    v.bar_plot_stat_per_time_period(period, name=None, stat=f'{stat}_count')
    v.plot_ranking_of_friends_by_message_stats()
