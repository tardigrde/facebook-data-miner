import json

import pandas as pd
import pytest

from miner.utils import decorators


def test_outputter():
    def mock_func(output: str = "json"):
        df = pd.DataFrame(
            {"num_legs": [2, 4,], "num_wings": [2, 0,]}, index=["falcon", "dog",]
        )
        return df

    res = decorators.outputter(mock_func)(output="json")
    assert isinstance(res, str)
    assert isinstance(json.loads(res), dict)


def test_kind_checker():
    def mock_func(kind: str = "private"):
        return True

    assert decorators.kind_checker(mock_func)(kind="private")

    assert decorators.kind_checker(mock_func)(kind="group")

    with pytest.raises(ValueError):
        decorators.kind_checker(mock_func)(kind="gibberish")


def test_column_checker():
    def mock_func(column: str = ""):
        return True

    with pytest.raises(ValueError):
        decorators.column_checker(mock_func)(column=1)


def test_period_checker():
    def mock_func(period: str = "y"):
        return True

    assert decorators.period_checker(mock_func)(period="y")

    assert decorators.period_checker(mock_func)(period="m")

    with pytest.raises(ValueError):
        decorators.period_checker(mock_func)(period="gibberish")


def test_attribute_checker():
    def mock_func(statistic: str = "mc"):
        return True

    assert decorators.attribute_checker(mock_func)(statistic="mc")

    assert decorators.attribute_checker(mock_func)(statistic="cc")

    with pytest.raises(ValueError):
        decorators.attribute_checker(mock_func)(statistic="gibberish")
