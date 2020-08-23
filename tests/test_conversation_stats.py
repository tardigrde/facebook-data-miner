def test_stats_are_in_df(analyzer):
    stats_df = analyzer.get_stats(names='Teflon Musk').get_conversation_statistics()

    assert 'msg_count' in stats_df
    assert 'text_msg_count' in stats_df
    assert 'media_count' in stats_df
    assert 'word_count' in stats_df
    assert 'unique_word_count' in stats_df
    assert 'char_count' in stats_df


def test_stats_index_can_be_grouped(analyzer):
    stats = analyzer.get_stats(names='Teflon Musk')
    assert stats.df.index[0].year == 2014
    assert stats.df.index[0].month == 9
    assert stats.df.index[0].day == 24
    assert stats.df.index[0].hour == 17


def test_get_time_series_data(analyzer):
    stats = analyzer.get_stats(names='Foo Bar')
    grouped = stats.get_grouped_time_series_data('y')
    assert len(grouped) == 1
    first_row = grouped.iloc[0]
    assert first_row.msg_count == 15
    assert first_row.media_count == 7
    assert first_row.word_count == 34
    assert first_row.unique_word_count == 34
    assert first_row.char_count == 140

    grouped = stats.get_grouped_time_series_data('m')
    assert len(grouped) == 5

    grouped = stats.get_grouped_time_series_data('d')
    assert len(grouped) == 9

    grouped = stats.get_grouped_time_series_data('h')
    assert len(grouped) == 14


def test_stats_per_period(analyzer):
    stats = analyzer.get_stats(names='Foo Bar')
    yearly = stats.stat_per_period('y', 'msg_count')
    assert yearly == {2020: 15}

    monthly = stats.stat_per_period('m', 'msg_count')
    assert monthly == {'april': 2, 'august': 1, 'february': 10, 'march': 1, 'may': 1}

    daily = stats.stat_per_period('d', 'msg_count')
    assert daily == {'monday': 1, 'tuesday': 2, 'wednesday': 1, 'thursday': 3, 'friday': 5, 'saturday': 2, 'sunday': 1}
    hourly = stats.stat_per_period('h', 'msg_count')
    assert hourly == {2: 1, 3: 1, 8: 1, 9: 1, 13: 2, 14: 5, 18: 2, 25: 1, 26: 1}


def test_ranking(analyzer):
    ranking = analyzer.stats.get_ranking_of_partners_by_messages()
    assert ranking == {'Foo Bar': 15, 'Tőke Hal': 7, 'Teflon Musk': 6, 'Benedek Elek': 3}
