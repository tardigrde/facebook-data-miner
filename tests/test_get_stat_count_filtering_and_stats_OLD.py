import pytest

from miner.utils.utils import dt


@pytest.fixture(scope="session")
def stat_count(panalyzer):
    return panalyzer.get_stat_count


def test_total_number_of_messages(stat_count):
    assert stat_count(attr="mc") == 31

    assert stat_count(attr="mc", start=dt(y=2000), period="y") == 0
    assert stat_count(attr="mc", start=dt(y=2014), period="y") == 13
    assert stat_count(attr="mc", start=dt(y=2018), period="y") == 3
    assert stat_count(attr="mc", start=dt(y=2020), period="y") == 15

    assert stat_count(attr="mc", start=dt(y=2011, m=11), period="m") == 0
    assert stat_count(attr="mc", start=dt(y=2014, m=9), period="m") == 1
    assert stat_count(attr="mc", start=dt(y=2014, m=11), period="m") == 10
    assert stat_count(attr="mc", start=dt(y=2014, m=12), period="m") == 2

    assert stat_count(attr="mc", start=dt(y=2018, m=1), period="m") == 3
    assert stat_count(attr="mc", start=dt(y=2018, m=5), period="m") == 0

    assert stat_count(attr="mc", start=dt(y=2020, m=2), period="m") == 10
    assert stat_count(attr="mc", start=dt(y=2020, m=3), period="m") == 1  # jpg
    assert stat_count(attr="mc", start=dt(y=2020, m=4), period="m") == 2
    assert stat_count(attr="mc", start=dt(y=2020, m=5), period="m") == 1
    assert stat_count(attr="mc", start=dt(y=2020, m=6), period="m") == 0
    assert stat_count(attr="mc", start=dt(y=2020, m=8), period="m") == 1

    assert stat_count(attr="mc", start=dt(y=2020, m=2, d=13), period="d") == 2
    assert (
        stat_count(attr="mc", start=dt(y=2020, m=2, d=13, h=5), period="h",)
        == 2
    )

    assert (
        stat_count(attr="mc", start=dt(y=2020, m=2, d=13, h=5), period="d",)
        == 4
    )


def test_total_number_of_words(stat_count):
    assert stat_count(attr="wc",) == 91

    assert stat_count(attr="wc", start=dt(y=2000), period="y") == 0
    assert stat_count(attr="wc", start=dt(y=2014), period="y") == 25
    assert stat_count(attr="wc", start=dt(y=2018), period="y") == 32
    assert stat_count(attr="wc", start=dt(y=2020), period="y") == 34

    assert stat_count(attr="wc", start=dt(y=2014, m=9), period="m") == 6
    assert stat_count(attr="wc", start=dt(y=2014, m=11), period="m") == 18
    assert stat_count(attr="wc", start=dt(y=2014, m=12), period="m") == 1

    assert stat_count(attr="wc", start=dt(y=2018, m=1), period="m") == 32
    assert stat_count(attr="wc", start=dt(y=2018, m=2), period="m") == 0

    assert stat_count(attr="wc", start=dt(y=2020, m=2), period="m") == 27
    assert stat_count(attr="wc", start=dt(y=2020, m=3), period="m") == 0
    assert stat_count(attr="wc", start=dt(y=2020, m=4), period="m") == 4
    assert stat_count(attr="wc", start=dt(y=2020, m=5), period="m") == 1
    assert stat_count(attr="wc", start=dt(y=2020, m=6), period="m") == 0
    assert stat_count(attr="wc", start=dt(y=2020, m=8), period="m") == 2

    assert stat_count(attr="wc", start=dt(y=2020, m=2, d=13), period="d") == 14
    assert (
        stat_count(attr="wc", start=dt(y=2020, m=2, d=13, h=5), period="d",)
        == 14
    )


def test_total_number_of_characters(stat_count):
    assert stat_count(attr="cc",) == 407

    assert stat_count(attr="cc", start=dt(y=2000), period="y") == 0
    assert stat_count(attr="cc", start=dt(y=2014), period="y") == 97
    assert stat_count(attr="cc", start=dt(y=2018), period="y") == 170
    assert stat_count(attr="cc", start=dt(y=2020), period="y") == 140

    assert stat_count(attr="cc", start=dt(y=2014, m=9), period="m") == 23
    assert stat_count(attr="cc", start=dt(y=2014, m=11), period="m") == 71
    assert stat_count(attr="cc", start=dt(y=2014, m=12), period="m") == 3

    assert stat_count(attr="cc", start=dt(y=2018, m=1), period="m") == 170
    assert stat_count(attr="cc", start=dt(y=2018, m=2), period="m") == 0

    assert stat_count(attr="cc", start=dt(y=2020, m=2), period="m") == 114
    assert stat_count(attr="cc", start=dt(y=2020, m=3), period="m") == 0
    assert stat_count(attr="cc", start=dt(y=2020, m=4), period="m") == 17
    assert stat_count(attr="cc", start=dt(y=2020, m=5), period="m") == 4
    assert stat_count(attr="cc", start=dt(y=2020, m=6), period="m") == 0
    assert stat_count(attr="cc", start=dt(y=2020, m=8), period="m") == 5


def test_total_number_of_messages_sent(stat_count):
    assert stat_count(attr="mc", senders="me",) == 18
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2014), period="y") == 7
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2018), period="y") == 2
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020), period="y") == 9
    )

    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2014, m=9), period="m",)
        == 1
    )
    assert (
        stat_count(
            attr="mc", senders="me", start=dt(y=2014, m=11), period="m",
        )
        == 5
    )
    assert (
        stat_count(
            attr="mc", senders="me", start=dt(y=2014, m=12), period="m",
        )
        == 1
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2018, m=1), period="m",)
        == 2
    )

    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2000), period="y") == 0
    )
    assert (
        stat_count(
            attr="mc", senders="me", start=dt(y=2011, m=11), period="m",
        )
        == 0
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2018, m=5), period="m",)
        == 0
    )

    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=2), period="m",)
        == 6
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=3), period="m",)
        == 0
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=4), period="m",)
        == 2
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=5), period="m",)
        == 0
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=6), period="m",)
        == 0
    )
    assert (
        stat_count(attr="mc", senders="me", start=dt(y=2020, m=8), period="m",)
        == 1
    )

    assert (
        stat_count(
            attr="mc", senders="me", start=dt(y=2020, m=2, d=13), period="d",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=5),
            period="h",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=18),
            period="h",
        )
        == 0
    )


def test_total_number_of_words_sent(stat_count):
    assert stat_count(attr="wc", senders="me",) == 71
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2000), period="y") == 0
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2014), period="y") == 18
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2018), period="y") == 31
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020), period="y") == 22
    )

    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2014, m=9), period="m",)
        == 6
    )
    assert (
        stat_count(
            attr="wc", senders="me", start=dt(y=2014, m=11), period="m",
        )
        == 11
    )
    assert (
        stat_count(
            attr="wc", senders="me", start=dt(y=2014, m=12), period="m",
        )
        == 1
    )

    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2018, m=1), period="m",)
        == 31
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2018, m=2), period="m",)
        == 0
    )

    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=2), period="m",)
        == 16
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=3), period="m",)
        == 0
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=4), period="m",)
        == 4
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=5), period="m",)
        == 0
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=6), period="m",)
        == 0
    )
    assert (
        stat_count(attr="wc", senders="me", start=dt(y=2020, m=8), period="m",)
        == 2
    )

    assert (
        stat_count(
            attr="wc", senders="me", start=dt(y=2020, m=2, d=13), period="d",
        )
        == 5
    )
    assert (
        stat_count(
            attr="wc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=5),
            period="h",
        )
        == 5
    )
    assert (
        stat_count(
            attr="wc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=7),
            period="h",
        )
        == 0
    )


def test_total_number_of_characters_sent(stat_count):
    assert stat_count(attr="cc", senders="me",) == 319

    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2000), period="y") == 0
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2014), period="y") == 68
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2018), period="y")
        == 167
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020), period="y") == 84
    )

    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2014, m=9), period="m",)
        == 23
    )
    assert (
        stat_count(
            attr="cc", senders="me", start=dt(y=2014, m=11), period="m",
        )
        == 42
    )
    assert (
        stat_count(
            attr="cc", senders="me", start=dt(y=2014, m=12), period="m",
        )
        == 3
    )

    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2018, m=1), period="m",)
        == 167
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2018, m=2), period="m",)
        == 0
    )

    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=2), period="m",)
        == 62
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=3), period="m",)
        == 0
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=4), period="m",)
        == 17
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=5), period="m",)
        == 0
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=6), period="m",)
        == 0
    )
    assert (
        stat_count(attr="cc", senders="me", start=dt(y=2020, m=8), period="m",)
        == 5
    )

    assert (
        stat_count(
            attr="cc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=5),
            period="d",
        )
        == 21
    )
    assert (
        stat_count(
            attr="cc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=7),
            period="d",
        )
        == 0
    )

    assert (
        stat_count(
            attr="cc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=5),
            period="h",
        )
        == 21
    )
    assert (
        stat_count(
            attr="cc",
            senders="me",
            start=dt(y=2020, m=2, d=13, h=7),
            period="h",
        )
        == 0
    )


def test_total_number_of_messages_received(stat_count):
    assert stat_count(attr="mc", senders="partner",) == 13
    assert (
        stat_count(attr="mc", senders="partner", start=dt(y=2000), period="y",)
        == 0
    )
    assert (
        stat_count(attr="mc", senders="partner", start=dt(y=2014), period="y",)
        == 6
    )
    assert (
        stat_count(attr="mc", senders="partner", start=dt(y=2018), period="y",)
        == 1
    )
    assert (
        stat_count(attr="mc", senders="partner", start=dt(y=2020), period="y",)
        == 6
    )

    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2011, m=11), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2014, m=9), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2014, m=11), period="m",
        )
        == 5
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2014, m=12), period="m",
        )
        == 1
    )

    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2018, m=1), period="m",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2018, m=5), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2020, m=2), period="m",
        )
        == 4
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2020, m=3), period="m",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2020, m=4), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2020, m=5), period="m",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc", senders="partner", start=dt(y=2020, m=8), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="mc",
            senders="partner",
            start=dt(y=2020, m=2, d=13),
            period="d",
        )
        == 1
    )
    assert (
        stat_count(
            attr="mc",
            senders="partner",
            start=dt(y=2020, m=2, d=14),
            period="d",
        )
        == 2
    )
    assert (
        stat_count(
            attr="mc",
            senders="partner",
            start=dt(y=2020, m=2, d=18),
            period="d",
        )
        == 1
    )


def test_total_number_of_words_received(stat_count):
    assert stat_count(attr="wc", senders="partner",) == 20

    assert (
        stat_count(attr="wc", senders="partner", start=dt(y=2000), period="y",)
        == 0
    )
    assert (
        stat_count(attr="wc", senders="partner", start=dt(y=2014), period="y",)
        == 7
    )
    assert (
        stat_count(attr="wc", senders="partner", start=dt(y=2018), period="y",)
        == 1
    )
    assert (
        stat_count(attr="wc", senders="partner", start=dt(y=2020), period="y",)
        == 12
    )

    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2014, m=9), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2014, m=11), period="m",
        )
        == 7
    )
    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2014, m=12), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2018, m=1), period="m",
        )
        == 1
    )
    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2018, m=2), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2020, m=2), period="m",
        )
        == 11
    )
    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2020, m=3), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="wc", senders="partner", start=dt(y=2020, m=5), period="m",
        )
        == 1
    )

    assert (
        stat_count(
            attr="wc",
            senders="partner",
            start=dt(y=2020, m=2, d=13),
            period="d",
        )
        == 9
    )
    assert (
        stat_count(
            attr="wc",
            senders="partner",
            start=dt(y=2020, m=2, d=14),
            period="d",
        )
        == 2
    )
    assert (
        stat_count(
            attr="wc",
            senders="partner",
            start=dt(y=2020, m=2, d=18),
            period="d",
        )
        == 0
    )


def test_total_number_of_characters_received(stat_count):
    assert stat_count(attr="cc", senders="partner",) == 88

    assert (
        stat_count(attr="cc", senders="partner", start=dt(y=2000), period="y",)
        == 0
    )
    assert (
        stat_count(attr="cc", senders="partner", start=dt(y=2014), period="y",)
        == 29
    )
    assert (
        stat_count(attr="cc", senders="partner", start=dt(y=2018), period="y",)
        == 3
    )
    assert (
        stat_count(attr="cc", senders="partner", start=dt(y=2020), period="y",)
        == 56
    )

    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2014, m=9), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2014, m=11), period="m",
        )
        == 29
    )
    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2014, m=12), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2018, m=1), period="m",
        )
        == 3
    )
    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2018, m=2), period="m",
        )
        == 0
    )

    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2020, m=2), period="m",
        )
        == 52
    )
    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2020, m=3), period="m",
        )
        == 0
    )
    assert (
        stat_count(
            attr="cc", senders="partner", start=dt(y=2020, m=5), period="m",
        )
        == 4
    )

    assert (
        stat_count(
            attr="cc",
            senders="partner",
            start=dt(y=2020, m=2, d=13),
            period="d",
        )
        == 30
    )
    assert (
        stat_count(
            attr="cc",
            senders="partner",
            start=dt(y=2020, m=2, d=14),
            period="d",
        )
        == 22
    )
    assert (
        stat_count(
            attr="cc",
            senders="partner",
            start=dt(y=2020, m=2, d=18),
            period="d",
        )
        == 0
    )
