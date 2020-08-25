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

    def set_up_time_series_data(self, stat="text_msg_count", **kwargs):
        stats = self.get_stats(**kwargs)
        return stats.get_conversation_statistics()[stat]

    def get_time_series_data(self, stat=None, subjects=[], **kwargs):
        subject_data = []
        for subject in subjects:
            data = self.set_up_time_series_data(stat=stat, subject=subject, **kwargs)
            subject_data.append(data)
        # TODO DATA HAS TO BE AUGMENTED FOR THIS TO WORK. y/m/d
        # df = pd.concat(subject_data, axis=1).fillna(0)
        # df.columns = subjects
        # return df
        return subject_data

    def get_stat_per_time_data(self, period, stat="msg_count", **kwargs):
        me_stat = self.get_stats(subject="me", **kwargs).stat_per_period(
            period, statistic=stat
        )
        partner_stat = self.get_stats(subject="partner", **kwargs).stat_per_period(
            period, statistic=stat
        )
        me_stat, partner_stat = utils.unify_dict_keys(me_stat, partner_stat)
        # TODO what is this??
        # sorting adds to otherwise empty keys...
        # me_stat = utils.sort_dict(me_stat, utils.PERIOD_MANAGER.sorting_method(period))
        # partner_stat = utils.sort_dict(partner_stat, utils.PERIOD_MANAGER.sorting_method(period))
        df = pd.DataFrame(
            {
                "date": list(me_stat.keys()),
                "me": list(me_stat.values()),
                "partner": list(partner_stat.values()),
            }
        )
        df = df.set_index("date")
        return df.index, df.me, df.partner

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
