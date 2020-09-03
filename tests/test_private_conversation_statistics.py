import pytest

from miner.utils import dt


@pytest.fixture(scope="session")
def priv_stats(priv_msg_analyzer):
    def _stats(**kwargs):
        if "names" in kwargs:
            analyzer = priv_msg_analyzer.filter(names=kwargs.get("names"))
        else:
            analyzer = priv_msg_analyzer
        if any([kw in kwargs for kw in ("channel", "subject", "start", "end")]):
            return analyzer.stats.filter(**kwargs)
        else:
            return analyzer.stats

    return _stats


class TestPrivateStatisticsWithFiltering:
    def test_stats_toke_hal_all(self, priv_stats):
        stats = priv_stats(channel="Tőke Hal")

        assert stats.mc == 7
        assert stats.unique_mc == 6
        # assert stats.most_used_msgs == 0
        assert stats.wc == 11
        assert stats.unique_wc == 9
        assert stats.cc == 47
        # assert stats.most_used_chars == 0

    def test_stats_toke_hal_me(self, priv_stats):
        stats = priv_stats(channel="Tőke Hal", subject="me")

        assert stats.mc == 4
        assert stats.unique_mc == 4
        # assert stats.most_used_msgs == 0
        assert stats.wc == 6
        assert stats.unique_wc == 5
        assert stats.cc == 22
        # assert stats.most_used_chars == 0

    def test_stats_toke_hal_partner(self, priv_stats):
        stats = priv_stats(channel="Tőke Hal", subject="partner")

        assert stats.mc == 3
        assert stats.unique_mc == 3
        # assert stats.most_used_msgs == 0
        assert stats.wc == 5
        assert stats.unique_wc == 5
        assert stats.cc == 25
        # assert stats.most_used_chars == 0

    def test_stats_toke_hal_all_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="all", start=dt(2014, 11), period="m"
        )

        assert stats.mc == 6
        assert stats.unique_mc == 5
        # assert stats.most_used_msgs == 0
        # assert stats.most_used_chars == 0

    def test_stats_toke_hal_partner_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="partner", start=dt(2014, 11), period="m"
        )
        assert stats.cc == 25
        assert stats.wc == 5

    def test_stats_toke_hal_me_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="me", start=dt(2014, 11), period="m"
        )
        assert stats.unique_wc == 5

    def test_stats_toke_hal_all_2014_12(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="all", start=dt(2014, 12), period="m"
        )
        assert stats.mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.unique_wc == 1
        assert stats.cc == 3
        # assert stats.most_used_chars == 0

    def test_stats_toke_hal_partner_2014_12(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="partner", start=dt(2014, 12), period="m"
        )
        assert stats.wc == 0

    def test_stats_toke_hal_me_2014_12(self, priv_stats):
        stats = priv_stats(
            channel="Tőke Hal", subject="me", start=dt(2014, 12), period="m"
        )
        assert stats.unique_mc == 1

    def test_stats_teflon_musk(self, priv_stats):
        stats = priv_stats(channel="Teflon Musk")
        assert stats.mc == 6
        assert stats.unique_mc == 2
        # assert stats.most_used_msgs == 0 # TODO LATER should only return the most used or e.g. top10 most used
        assert stats.wc == 14
        assert stats.unique_wc == 7
        assert stats.cc == 52  # 23
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me(self, priv_stats):
        stats = priv_stats(channel="Teflon Musk", subject="me")
        assert stats.mc == 3
        assert stats.unique_mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 12
        assert stats.unique_wc == 6
        assert stats.cc == 48
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_partner(self, priv_stats):
        stats = priv_stats(channel="Teflon Musk", subject="partner")
        assert stats.mc == 3
        assert stats.unique_mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 2
        assert stats.unique_wc == 1
        assert stats.cc == 4
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_all_2014_9(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="all", start=dt(2014, 9), period="m"
        )
        assert stats.mc == 1
        # assert stats.most_used_msgs == 0
        assert stats.wc == 6
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_9(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="me", start=dt(2014, 9), period="m"
        )
        assert stats.unique_wc == 6

    def test_stats_teflon_musk_partner_2014_9(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="partner", start=dt(2014, 9), period="m"
        )
        assert stats.unique_mc == 0
        assert stats.cc == 0

    def test_stats_teflon_musk_all_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="all", start=dt(2014, 11), period="m"
        )
        assert stats.mc == 4
        # assert stats.most_used_msgs == 0
        # assert stats.most_used_chars == 0

    def test_stats_teflon_musk_me_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="me", start=dt(2014, 11), period="m"
        )
        assert stats.wc == 6

    def test_stats_teflon_musk_partner_2014_11(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="partner", start=dt(2014, 11), period="m"
        )
        assert stats.unique_mc == 1
        assert stats.unique_wc == 1
        assert stats.cc == 4

    def test_stats_teflon_musk_all_2014_12(self, priv_stats):
        stats = priv_stats(
            channel="Teflon Musk", subject="all", start=dt(2014, 12), period="m"
        )

        assert stats.mc == 1
        assert stats.unique_mc == 0
        # assert stats.most_used_msgs == 0
        assert stats.wc == 0
        assert stats.unique_wc == 0
        assert stats.cc == 0
        # assert stats.most_used_chars == 0
