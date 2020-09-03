import pytest
from datetime import datetime
import numpy as np
import pandas as pd

from miner.message.conversation_analyzer import MessagingAnalyzerManager
from miner.message.conversations import Conversations
from miner.message.conversation_stats import (
    ConversationStats,
    PrivateConversationStats,
    GroupConversationStats,
)


@pytest.fixture
def priv_stats(priv_msg_analyzer):
    return priv_msg_analyzer.stats


@pytest.fixture(scope="module")
def group_stats(group_msg_analyzer):
    return group_msg_analyzer.stats


class TestGroupConversationStats:
    def test_general_stats_again(self, group_stats):
        assert isinstance(group_stats, GroupConversationStats)

        assert group_stats.mc == 18
        assert group_stats.media_mc == 2
        assert group_stats.wc == 40
        assert "marathon" in list(group_stats.groups)
        assert isinstance(group_stats.start, datetime)

    def test_filter(self):
        pass

    def test_names_and_groups(self):
        pass

    def test_get_most_used_messages(self):
        pass

    def test_get_grouped_time_series_data(self):
        pass

    def test_stat_per_period(self):
        pass

    def test_number_of_groups_in_stats(self, group_stats):
        assert group_stats.number_of_groups == 3

    def test_contributors(self, group_stats):
        contributors = group_stats.contributors
        assert "Foo Bar" in contributors
        assert "Facebook User" in contributors  # TODO??

        assert group_stats.number_of_contributors == 8


class TestPrivateConversationStats:
    def test_stats_are_in_df(self, priv_msg_analyzer):
        stats_df = priv_msg_analyzer.filter(
            names="Teflon Musk"
        ).stats.get_conversation_statistics()

        assert "mc" in stats_df
        assert "text_mc" in stats_df
        assert "media_mc" in stats_df
        assert "wc" in stats_df
        assert "cc" in stats_df

    def test_stats_index_can_be_grouped(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(names="Teflon Musk").stats
        assert stats.df.index[0].year == 2014
        assert stats.df.index[0].month == 9
        assert stats.df.index[0].day == 24
        assert stats.df.index[0].hour == 17

    def test_get_time_series_data(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(names="Foo Bar").stats
        grouped = stats.get_grouped_time_series_data("y")
        assert len(grouped) == 1
        first_row = grouped.iloc[0]
        assert first_row.mc == 15
        assert first_row.media_mc == 7
        assert first_row.wc == 34
        assert first_row.cc == 140

        grouped = stats.get_grouped_time_series_data("m")
        assert len(grouped) == 5

        grouped = stats.get_grouped_time_series_data("d")
        assert len(grouped) == 9

        grouped = stats.get_grouped_time_series_data("h")
        assert len(grouped) == 14

    def test_stats_per_period(self, priv_msg_analyzer):
        stats = priv_msg_analyzer.filter(names="Foo Bar").stats
        yearly = stats.stat_per_period("y", "mc")
        assert yearly == {
            2009: 0,
            2010: 0,
            2011: 0,
            2012: 0,
            2013: 0,
            2014: 0,
            2015: 0,
            2016: 0,
            2017: 0,
            2018: 0,
            2019: 0,
            2020: 15,
        }

        monthly = stats.stat_per_period("m", "mc")
        assert monthly == {
            "january": 0,
            "february": 10,
            "march": 1,
            "april": 2,
            "may": 1,
            "june": 0,
            "july": 0,
            "august": 1,
            "september": 0,
            "october": 0,
            "november": 0,
            "december": 0,
        }

        daily = stats.stat_per_period("d", "mc")
        assert daily == {
            "monday": 1,
            "tuesday": 2,
            "wednesday": 1,
            "thursday": 3,
            "friday": 5,
            "saturday": 2,
            "sunday": 1,
        }
        hourly = stats.stat_per_period("h", "mc")
        assert hourly == {
            0: 1,
            1: 1,
            2: 0,
            3: 0,
            4: 1,
            5: 0,
            6: 2,
            7: 0,
            8: 1,
            9: 0,
            10: 0,
            11: 1,
            12: 2,
            13: 1,
            14: 0,
            15: 1,
            16: 0,
            17: 0,
            18: 1,
            19: 0,
            20: 2,
            21: 0,
            22: 0,
            23: 1,
        }

    def test_properties(self, priv_stats):
        percentage_of_media_msgs = priv_stats.percentage_of_media_messages
        assert percentage_of_media_msgs == pytest.approx(29.03, 0.1)

    def test_get_grouped_time_series_data(self, priv_msg_analyzer):
        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="y")
        assert len(grouped) == 3
        third_row = grouped.iloc[2]
        assert third_row.mc == 15
        assert third_row.media_mc == 7
        assert third_row.wc == 34
        assert third_row.cc == 140

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="m")
        assert len(grouped) == 9

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="d")
        assert len(grouped) == 16

        grouped = priv_msg_analyzer.stats.get_grouped_time_series_data(period="h")
        assert len(grouped) == 24

    def test_ranking(self, priv_msg_analyzer):
        ranking = priv_msg_analyzer.get_ranking_of_partners_by_convo_stats()
        assert ranking == {
            "Foo Bar": 15,
            "Tőke Hal": 7,
            "Teflon Musk": 6,
            "Benedek Elek": 3,
        }

    def test_stats_per_period(self, priv_msg_analyzer):
        yearly = priv_msg_analyzer.stats.stat_per_period("y", "mc")
        assert yearly == {
            2009: 0,
            2010: 0,
            2011: 0,
            2012: 0,
            2013: 0,
            2014: 13,
            2015: 0,
            2016: 0,
            2017: 0,
            2018: 3,
            2019: 0,
            2020: 15,
        }

        monthly = priv_msg_analyzer.stats.stat_per_period("m", "mc")
        assert monthly == {
            "january": 3,
            "february": 10,
            "march": 1,
            "april": 2,
            "may": 1,
            "june": 0,
            "july": 0,
            "august": 1,
            "september": 1,
            "october": 0,
            "november": 10,
            "december": 2,
        }

        daily = priv_msg_analyzer.stats.stat_per_period("d", "mc")
        assert daily == {
            "monday": 6,
            "tuesday": 2,
            "wednesday": 6,
            "thursday": 3,
            "friday": 6,
            "saturday": 3,
            "sunday": 5,
        }

        hourly = priv_msg_analyzer.stats.stat_per_period("h", "mc")
        assert hourly == {
            0: 1,
            1: 1,
            2: 1,
            3: 0,
            4: 1,
            5: 0,
            6: 2,
            7: 0,
            8: 1,
            9: 1,
            10: 0,
            11: 1,
            12: 7,
            13: 1,
            14: 0,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 4,
            21: 0,
            22: 2,
            23: 3,
        }
