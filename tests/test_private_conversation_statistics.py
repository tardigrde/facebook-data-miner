import pandas as pd

from miner.utils.utils import dt


class TestPrivateStatisticsWithFiltering:
    def test_stats_toke_hal_all(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats

        assert stats.mc == 7
        assert stats.wc == 11
        assert stats.cc == 47
        assert stats.unique_mc == 6
        assert stats.unique_wc == 9
        assert isinstance(stats.most_used_msgs, pd.DataFrame)
        assert list(stats.most_used_msgs.columns) == ["unique_values", "counts"]
        assert stats.most_used_msgs.iloc[0].unique_values == "yo"

    def test_stats_toke_hal_me(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(senders="me")

        assert stats.mc == 4
        assert stats.wc == 6
        assert stats.cc == 22
        assert stats.unique_mc == 4
        assert stats.unique_wc == 5
        assert stats.most_used_msgs.shape == (4, 2)
        assert stats.most_used_msgs.iloc[0].counts == 1

    def test_stats_toke_hal_partner(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(senders="partner")

        assert stats.mc == 3
        assert stats.wc == 5
        assert stats.cc == 25
        assert stats.unique_mc == 3
        assert stats.unique_wc == 5
        assert isinstance(stats.most_used_words, pd.DataFrame)
        assert stats.most_used_words.shape == (5, 2)

    def test_stats_toke_hal_all_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            start=dt(2014, 11), period="m"
        )
        assert stats.mc == 6
        assert stats.unique_mc == 5

    def test_stats_toke_hal_partner_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            senders="partner", start="2014-11-1", period="m"
        )
        assert stats.cc == 25
        assert stats.wc == 5

    def test_stats_toke_hal_me_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            senders="me", start=dt(2014, 11), period="m"
        )
        assert stats.unique_wc == 5

    def test_stats_toke_hal_all_2014_12(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            start="2014-12-1", period="m"
        )
        assert stats.mc == 1
        assert stats.cc == 3
        assert stats.unique_wc == 1

    def test_stats_toke_hal_partner_2014_12(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            senders="partner", start=dt(2014, 12), period="m"
        )
        assert stats.wc == 0

    def test_stats_toke_hal_me_2014_12(self, panalyzer):
        stats = panalyzer.filter(channels="Tőke Hal").stats.filter(
            senders="me", start="2014-12-1", period="m"
        )
        assert stats.unique_mc == 1

    def test_stats_teflon_musk(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats
        assert stats.mc == 6
        assert stats.wc == 14
        assert stats.cc == 50
        assert stats.unique_mc == 2
        assert stats.unique_wc == 7

    def test_stats_teflon_musk_me(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(senders="me")
        assert stats.mc == 3
        assert stats.wc == 12
        assert stats.cc == 46
        assert stats.unique_mc == 1
        assert stats.unique_wc == 6

    def test_stats_teflon_musk_partner(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(senders="partner")
        assert stats.mc == 3
        assert stats.wc == 2
        assert stats.cc == 4
        assert stats.unique_mc == 1
        assert stats.unique_wc == 1

    def test_stats_teflon_musk_all_2014_9(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            start=dt(2014, 9), period="m"
        )
        assert stats.mc == 1
        assert stats.wc == 6

    def test_stats_teflon_musk_me_2014_9(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            senders="me", start="2014-9-1", period="m"
        )
        assert stats.unique_wc == 6

    def test_stats_teflon_musk_partner_2014_9(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            senders="partner", start=dt(2014, 9), period="m"
        )
        assert stats.unique_mc == 0
        assert stats.cc == 0

    def test_stats_teflon_musk_all_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            start="2014-11-1", period="m"
        )
        assert stats.mc == 4

    def test_stats_teflon_musk_me_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            senders="me", start=dt(2014, 11), period="m"
        )
        assert stats.wc == 6

    def test_stats_teflon_musk_partner_2014_11(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            senders="partner", start="2014-11-1", period="m"
        )
        assert stats.cc == 4
        assert stats.unique_mc == 1
        assert stats.unique_wc == 1

    def test_stats_teflon_musk_all_2014_12(self, panalyzer):
        stats = panalyzer.filter(channels="Bugs Bunny").stats.filter(
            start=dt(2014, 12), period="m"
        )
        assert stats.mc == 1
        assert stats.wc == 0
        assert stats.cc == 0
        assert stats.unique_mc == 0
        assert stats.unique_wc == 0
