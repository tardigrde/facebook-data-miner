import json
import os
import tempfile

import pytest
import pytz
from helpers import lower_string, add_string, split_string, tempfile_tree

from miner.utils import utils, command


@pytest.fixture(scope="session")
def tempfiles():
    return tempfile_tree()


@pytest.fixture(scope="module")
def command_chain():
    ccc = command.CommandChainCreator()
    ccc.register_command(utils.decode_data, utils.utf8_decoder)
    ccc.register_command(lower_string)
    ccc.register_command(add_string, addition="abc")
    ccc.register_command(utils.replace_accents)
    ccc.register_command(split_string)

    return ccc


class TestCommandChainCreator:
    def test_register_commands(self, command_chain):
        command_chain("test")
        assert len(command_chain.commands) == 5

    def test_commands_applied(self, command_chain):
        res = command_chain("T\u00c5\u0091ke Hal")
        assert res == ["toke", "halabc"]


class TestUtils:
    def test_ts_to_date(self, tz_name):
        dt = 1454607689000

        target_tz = pytz.timezone(tz_name)

        with_tz = utils.ts_to_date(dt, target_tz)

        expected_date = utils.dt(
            y=2016, m=2, d=4, h=17, minute=41, second=29, tz=target_tz
        )
        assert expected_date == with_tz

    def test_ts_to_date_and_dt(self, tz_name):
        date = 1598046630000

        target_tz = pytz.timezone(tz_name)
        with_tz = utils.ts_to_date(date, target_tz)
        # Friday, August 21, 2020 9:50:30 PM
        expected_date = utils.dt(
            y=2020, m=8, d=21, h=21, minute=50, second=30, tz=target_tz
        )
        assert expected_date == with_tz

    # THIS DOES NOT WORK ON WINDOWS
    def test_walk_directory_and_search_jsons(self, tempfiles):
        jsons_found = utils.walk_directory_and_search(
            "/tmp", utils.get_all_jsons, ".json", ""
        )
        assert len(tempfiles) == 5

        assert len(list(set(tempfiles) & set(jsons_found))) == 5

    def test_walk_directory_and_search_dirs_that_contain_(self):
        parent = utils.walk_directory_and_search(
            "/tmp",
            utils.get_parent_directory_of_file_with_extension,
            ".json",
            "",
        )
        assert "/tmp" in list(parent)

    def test_fill_dict_and_sort_dict(self):
        unsorted = {}
        unsorted = utils.fill_dict(unsorted, "b", 3)
        unsorted = utils.fill_dict(unsorted, "a", 2)
        unsorted = utils.fill_dict(unsorted, "c", 4)
        unsorted = utils.fill_dict(unsorted, "a", 3)
        assert unsorted == {"b": 3, "a": 5, "c": 4}
        sorted_desc = utils.sort_dict(
            unsorted, func=lambda item: item[1], reverse=False
        )
        assert sorted_desc == {"b": 3, "c": 4, "a": 5}
        sorted_asc = utils.sort_dict(
            sorted_desc, func=lambda item: item[1], reverse=True
        )
        assert sorted_asc == {"a": 5, "c": 4, "b": 3}

    def test_unzip(self):
        f = tempfile.NamedTemporaryFile()
        path = utils.unzip(f.name)
        assert path == f.name

        # Won't test ZipFile code

    def test_basedir_exists(self):
        res = utils.basedir_exists(os.path.realpath(__file__))
        assert res

        res = utils.basedir_exists("/home/whatever/a/gibberish")
        assert not res

    def test_df_to_file(self, sample_df):
        path = f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}test.csv"

        res = utils.df_to_file(path, sample_df)
        assert res == f"Data was written to {path}"
        os.unlink(path)

        path = (
            f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}test.json"
        )
        res = utils.df_to_file(path, sample_df)
        assert res == f"Data was written to {path}"
        os.unlink(path)

        path = "csv"
        res = utils.df_to_file(path, sample_df)
        assert isinstance(res, str)

        path = "json"
        res = utils.df_to_file(path, sample_df)
        assert isinstance(res, str)
        assert isinstance(json.loads(res), dict)

        res = utils.df_to_file("/home/whatever/a/gibberish", sample_df)
        assert res == "Directory does not exist: `/home/whatever/a`"

    def test_get_start_based_on_period(self):
        res = utils.get_start_based_on_period(utils.dt(2014, 2, 2), "y")
        assert res == utils.dt(2014, 1, 1)

        res = utils.get_start_based_on_period(utils.dt(2014, 2, 2), "m")
        assert res == utils.dt(2014, 2, 1)

    def test_remove_items_where_value_is_falsible(self):
        res = utils.remove_items_where_value_is_falsible({1: 0, 2: 1, 3: 2})
        assert res == {2: 1, 3: 2}

    def test_generate_date_series(self):
        res = utils.generate_date_series(utils.dt(2010, 10, 10))
        expected = [utils.dt(i, 2, 4) for i in range(2004, 2021)]
        assert res == expected


class TestDataFrameUtils:
    def test_stack_dfs(self):
        pass

    def test_filter_by_date(self, friends, tz_name):
        df = friends.data

        filtered = utils.filter_by_date(
            df,
            start=utils.dt(y=2020, m=3, d=1, tz=pytz.timezone(tz_name)),
            end=utils.dt(y=2020, m=4, d=30, tz=pytz.timezone(tz_name)),
        )
        assert len(filtered) == 3

        filtered = utils.filter_by_date(
            df, start="2020-03-01", end="2020-04-30"
        )
        assert len(filtered) == 3

    def test_df_to_str(self, sample_df):
        res = utils.df_to_str("csv", sample_df)
        assert isinstance(res, str)
        assert ",num_legs,num_wings" in res

        res = utils.df_to_str("json", sample_df)
        assert isinstance(res, str)
        assert isinstance(json.loads(res), dict)
