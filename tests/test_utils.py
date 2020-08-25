from datetime import datetime
import tempfile
import pytest
import os

from miner import utils
from helpers import lower_string, add_string, split_string, tempfile_tree

TEST_DATA_PATH = f"{os.getcwd()}/test_data"


@pytest.fixture(scope="session")
def tempfiles():
    return tempfile_tree()


@pytest.fixture(scope="module")
def command_chain():
    ccc = utils.CommandChainCreator()
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
    def test_ts_to_date_and_dt(self):
        date = 1598046630000
        expected_date = utils.dt(
            year=2020, month=8, day=21, hour=23, minute=50, second=30
        )
        assert expected_date == utils.ts_to_date(date)

    def test_walk_directory_and_search_dirs_that_contain_(self):
        parent = utils.walk_directory_and_search(
            "/tmp", utils.get_parent_directory_of_file, ".json", ""
        )
        assert "/tmp" in list(parent)

    def test_walk_directory_and_search_jsons(self, tempfiles):
        jsons_found = utils.walk_directory_and_search(
            "/tmp", utils.get_all_jsons, ".json", ""
        )
        assert len(tempfiles) == 5
        assert len(list(set(tempfiles) & set(jsons_found))) == 5


class TestDataFrameUtils:
    def test_stack_dfs(self):
        pass

    def test_filter_by_date(self, friends):
        df = friends.data

        filtered = utils.filter_by_date(
            df,
            start=utils.dt(year=2020, month=3, day=1),
            end=utils.dt(year=2020, month=4, day=30),
        )
        assert len(filtered) == 3

        filtered = utils.filter_by_date(df, start="2020-03-01", end="2020-04-30")
        assert len(filtered) == 3
