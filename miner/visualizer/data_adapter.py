import pandas as pd

from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.message.conversations import Conversations
from miner.people import People

from miner import utils


class DataAdapter:
    """
    Class for adopting statistics data for Visualizer to use.
    """

    def __init__(self, path):
        self.path = path
        self.analyzer = self.get_analyzer()
        self.stats = self.get_stats()

    def get_analyzer(self):
        convos = Conversations(path=self.path)
        return ConversationAnalyzer(convos)

    def get_stats(self, **kwargs):
        analyzer = self.get_analyzer()
        return analyzer.get_stats(**kwargs)

    def set_up_time_series_data(self, period, stat="text_msg_count", **kwargs):
        stats = self.get_stats(**kwargs)
        return stats.get_grouped_time_series_data(period)[stat]

    def get_time_series_data(self, period, stat=None, **kwargs):
        index, me, partner = self.get_stat_per_time_data(period, stat)
        utils.generate_date_series(period, start=index[0], end=index[-1])
        print()

    def get_stat_per_time_data(self, period, stat="msg_count", **kwargs):
        me_stat = self.get_stats(subject="me", **kwargs).stat_per_period(
            period, statistic=stat
        )
        partner_stat = self.get_stats(subject="partner", **kwargs).stat_per_period(
            period, statistic=stat
        )
        return list(me_stat.keys()), list(me_stat.values()), list(partner_stat.values())

    def get_ranking_of_friends_by_message_stats(self, stat="msg_count"):
        analyzer = self.get_analyzer()
        ranks_dict = analyzer.get_ranking_of_partners_by_messages(statistic=stat)
        # TODO watch out; might be not working correctly; check upper function
        sorted_dict = utils.sort_dict(
            ranks_dict, func=lambda item: item[1], reverse=True,
        )
        sliced_dict = (
            utils.slice_dict(sorted_dict, 20) if len(sorted_dict) > 20 else sorted_dict
        )
        cleared_dict = utils.remove_items_where_value_is_falsible(sliced_dict)

        df = pd.DataFrame(cleared_dict, index=[0])
        return list(df.columns), df.iloc[0]
