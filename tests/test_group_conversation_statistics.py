import pytest

from miner.utils import dt
from miner.message.conversation_stats import (
    ConversationStats,
    PrivateConversationStats,
    GroupConversationStats,
)


@pytest.fixture(scope="session")
def group_stats(group_msg_analyzer):
    def _stats(**kwargs):
        if "names" in kwargs:
            analyzer = group_msg_analyzer.filter(names=kwargs.get("names"))
        else:
            analyzer = group_msg_analyzer
        if any([kw in kwargs for kw in ("channel", "subject", "start", "end")]):
            return analyzer.stats.filter(**kwargs)
        else:
            return analyzer.stats

    return _stats


class TestGroupStatisticsWithFiltering:
    def test_stats_group_stats_props(self, group_msg_analyzer):
        stats = group_msg_analyzer.stats
        for prop in [
            "audios",
            "cc",
            "contributors",
            "created_by_me",
            "creator",
            "df",
            "end",
            "files",
            "filter",
            "get_conversation_statistics",
            "get_filtered_df",
            "get_grouped_time_series_data",
            "get_most_used_messages",
            "get_words",
            "gifs",
            "groups",
            "mc",
            "media",
            "media_mc",
            "messages",
            "most_used_msgs",
            "most_used_words",
            "multi",
            "names",
            "number_of_contributors",
            "number_of_groups",
            "percentage_of_media_messages",
            "photos",
            "start",
            "stat_per_period",
            "text_mc",
            "unique_mc",
            "unique_wc",
            "videos",
            "wc",
            "words",
        ]:
            assert getattr(stats, prop) is not None

    def test_stats_marathon(self, group_msg_analyzer):
        stats = group_msg_analyzer.filter(groups="marathon").stats

        assert isinstance(stats, GroupConversationStats)

        assert stats.mc == 9
        assert stats.text_mc == 7
        assert stats.media_mc == 2
        assert stats.wc == 21
        assert stats.cc == 86

        assert stats.unique_mc == 7
        assert stats.unique_wc == 19

    def test_stats_biggest_group_filtered(self, group_msg_analyzer):
        group_stats = group_msg_analyzer.filter(
            groups="Tőke Hal, Foo Bar, Donald Duck and 2 others"
        ).stats

        filtered_stats_me = group_stats.filter(subject="me")
        assert filtered_stats_me.mc == 0

        filtered_stats_from_2011_07_17_15h = group_stats.filter(
            start=dt(y=2011, m=7, d=17, h=15, minute=0, second=30), period="y"
        )
        assert filtered_stats_from_2011_07_17_15h.mc == 3
