import pytest

from miner.utils.utils import dt
from miner.message.conversation_stats import ConversationStats


@pytest.fixture(scope="session")
def group_stats(group_msg_analyzer):
    def _stats(**kwargs):
        if "names" in kwargs:
            analyzer = group_msg_analyzer.filter(participants=kwargs.get("names"))
        else:
            analyzer = group_msg_analyzer
        if any([kw in kwargs for kw in ("channel", "subject", "start", "end")]):
            return analyzer._stats.filter(**kwargs)
        else:
            return analyzer._stats

    return _stats


class TestGroupStatisticsWithFiltering:
    def test_stats_marathon(self, group_msg_analyzer):
        stats = group_msg_analyzer.filter(channels="marathon")._stats

        assert isinstance(stats, ConversationStats)

        assert stats.mc == 9
        assert stats.text_mc == 7
        assert stats.media_mc == 2
        assert stats.wc == 21
        assert stats.cc == 86

        assert stats.unique_mc == 7
        assert stats.unique_wc == 19

    def test_stats_biggest_group_filtered(self, group_msg_analyzer):
        group_stats = group_msg_analyzer.filter(
            channels="Tőke Hal, Foo Bar, Donald Duck and 2 others"
        )._stats

        filtered_stats_me = group_stats.filter(senders="me")
        assert filtered_stats_me.mc == 0

        filtered_stats_from_2011_07_17_15h = group_stats.filter(
            start=dt(y=2011, m=7, d=17, h=15, minute=0, second=30), period="y"
        )
        assert filtered_stats_from_2011_07_17_15h.mc == 3
