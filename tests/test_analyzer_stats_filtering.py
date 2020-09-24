import pytest

from miner.utils import utils


class TestAnalyzerStatsFiltering:
    def test_private_analyzer_stats(self, analyzer):
        a = analyzer.private
        s = analyzer.private.stats
        assert len(a) == len(s.channels)
        assert all([c in a.participants for c in s.contributors])
        assert a.stats.df.shape == s.df.shape

    def test_group_analyzer_stats(self, analyzer):
        a = analyzer.group
        s = analyzer.group.stats
        assert len(a) == len(s.channels)
        assert all([c in a.participants for c in s.contributors])

    def test_private_analyzer_filter(self, analyzer):
        afc = analyzer.private.filter(channels="Teflon Musk")
        afp = analyzer.private.filter(participants="Teflon Musk")
        assert len(afc) == len(afp)
        assert len(afc.participants) == len(afp.participants)
        assert afc.number_of_convos_created_by_me == afp.number_of_convos_created_by_me
        assert afc.stats.df.shape == afp.stats.df.shape

        afc = analyzer.private.filter(channels=["Teflon Musk", "Foo Bar"])
        afp = analyzer.private.filter(participants=["Teflon Musk", "Foo Bar"])
        assert len(afc) == len(afp)
        assert len(afc.participants) == len(afp.participants)
        assert afc.number_of_convos_created_by_me == afp.number_of_convos_created_by_me
        assert len(afc.get_ranking_of_people_by_convo_stats().get("count")) == len(
            afp.get_ranking_of_people_by_convo_stats().get("count")
        )

    def test_group_analyzer_filter(self, analyzer):
        afc = analyzer.group.filter(channels="marathon")
        afp = analyzer.group.filter(participants="Teflon Musk")
        assert len(afc) != len(afp)
        assert len(afc.participants) != len(afp.participants)
        assert afc.number_of_convos_created_by_me != afp.number_of_convos_created_by_me

    def test_group_analyzer_filter_switched_kwargs(self, analyzer, caplog):
        afc = analyzer.group.filter(channels="Teflon Musk")
        afp = analyzer.group.filter(participants="marathon")
        assert len(afc) == 0
        assert len(afp) == 0

    def test_filter_me_as_participant(self, analyzer):
        afcpm = analyzer.private.filter(
            channels="Teflon Musk", participants="Levente Csőke"
        )
        afcp = analyzer.private.filter(
            channels="Teflon Musk", participants="Teflon Musk"
        )
        assert len(afcpm) == len(afcp)
        assert len(afcpm.participants) == len(afcp.participants)
        assert (
            afcpm.number_of_convos_created_by_me == afcp.number_of_convos_created_by_me
        )
        with pytest.raises(utils.TooFewPeopleError):
            assert len(
                afcpm.get_ranking_of_people_by_convo_stats().get("count")
            ) == len(afcp.get_ranking_of_people_by_convo_stats().get("count"))

    def test_group_analyzer_filter_channels_participants(self, analyzer):
        afc = analyzer.group.filter(channels=["marathon"])
        afp = analyzer.group.filter(participants=["Teflon Musk", "Foo Bar"])
        assert len(afp) != len(afc)
        assert len(afp.participants) != len(afc.participants)
        assert afp.number_of_convos_created_by_me != afc.number_of_convos_created_by_me
        assert len(afp.get_ranking_of_people_by_convo_stats().get("count")) != len(
            afc.get_ranking_of_people_by_convo_stats().get("count")
        )

    def test_private_analyzer_stats_filter(self, analyzer):
        afc = analyzer.private.filter(channels="Teflon Musk")
        sfp = analyzer.private.stats.filter(channels="Teflon Musk",)
        assert len(afc.stats.df) == len(sfp)
        assert len(afc.participants) == len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 1 if sfp.created_by_me else 0
        assert (
            afc.stats.df.shape == sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

        # same
        afc = analyzer.private.filter(participants="Teflon Musk")
        sfp = analyzer.private.stats.filter(channels="Teflon Musk")
        assert len(afc.stats.df) == len(sfp)
        assert len(afc.participants) == len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 1 if sfp.created_by_me else 0
        assert (
            afc.stats.df.shape == sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

    def test_private_analyzer_stats_filter_by_senders(self, analyzer):
        afc = analyzer.private.filter(channels="Teflon Musk")
        sfp = analyzer.private.stats.filter(
            channels="Teflon Musk", senders=["Teflon Musk", "Levente Csőke"]
        )
        assert len(afc.stats.df) == len(sfp)
        assert len(afc.participants) == len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 1
        assert sfp.contributors == ["Levente Csőke", "Teflon Musk"]
        assert (
            afc.stats.df.shape == sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

        afc = analyzer.private.filter(participants="Teflon Musk")
        sfp = analyzer.private.stats.filter(
            channels="Teflon Musk", senders="Teflon Musk"
        )
        assert len(afc.stats.df) > len(sfp)
        assert len(afc.participants) > len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 1
        assert sfp.contributors == ["Teflon Musk"]
        assert not sfp.created_by_me

    def test_group_analyzer_stats_filter_by_channel(self, analyzer):
        afc = analyzer.group.filter(channels="marathon")
        sfp = analyzer.group.stats.filter(channels="marathon")
        assert len(afc.stats.df) == len(sfp)
        assert len(afc.participants) == 4
        assert len(sfp.contributors) == 3
        assert afc.number_of_convos_created_by_me == 1
        assert (
            afc.stats.df.shape == sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

    def test_group_analyzer_stats_filter_by_sender_participant(self, analyzer):
        afc = analyzer.group.filter(participants="Teflon Musk")
        sfp = analyzer.group.stats.filter(senders="Teflon Musk")
        assert len(afc.stats.df) > len(sfp)
        assert len(afc.participants) > len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 2
        assert (
            afc.stats.df.shape != sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

    def test_group_analyzer_stats_filter_by_senders(self, analyzer):
        afc = analyzer.group.filter(channels="Teflon Musk")
        sfp = analyzer.group.stats.filter(
            channels="Teflon Musk", senders=["Teflon Musk", "Levente Csőke"]
        )
        assert len(afc.stats.df) == len(sfp)
        assert len(afc.participants) == len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 0
        assert (
            afc.stats.df.shape == sfp.df.shape
        )  # should be the same but now columns are not the same; see _get_filtered_df

        afc = analyzer.group.filter(participants="Teflon Musk")
        sfp = analyzer.group.stats.filter(channels="Teflon Musk", senders="Teflon Musk")
        assert len(afc.stats.df) > len(sfp)
        assert len(afc.participants) > len(sfp.contributors)
        assert afc.number_of_convos_created_by_me == 2
        assert not sfp.created_by_me

    def test_anaylzer_filter_returns_none(self, analyzer):
        afc = analyzer.group.filter(channels="Teflon Musk")
        assert not len(afc)
        afp = analyzer.group.filter(participants="marathon")
        assert not len(afp)

    def test_empty_df(self, analyzer):
        sfp = analyzer.group.stats.filter(channels="Teflon Musk")
        assert len(sfp) == 0

        sfs = analyzer.group.stats.filter(senders="marathon")
        assert len(sfs) == 0
