import copy
import inspect
import json
import logging
import math
import os
import re
import time
import zipfile
from datetime import datetime
from itertools import islice
from typing import Union, List, Dict, Callable

import pandas as pd

from miner.utils import const, decorators


class TooFewPeopleError(Exception):
    pass


class TooManyChannelsError(Exception):
    pass


class NonExistentChannel(Exception):
    pass


def get_properties_of_a_class(class_ref):
    props = inspect.getmembers(class_ref, lambda o: isinstance(o, property))
    return [p[0] for p in props]


def get_group_convo_map(data):
    group_convo_map = {}
    if not data:
        return group_convo_map
    for channel, convo in data.items():
        for participant in convo.metadata.participants:
            group_convo_map = fill_dict(group_convo_map, participant, [channel])
            group_convo_map[participant] = list(
                set(group_convo_map.get(participant))
            )  # just making sure there is no duplicate, so I don't have to go over it again later
    return group_convo_map


def get_period_map(join_date):
    const.PERIOD_MAP["y"] = list(range(join_date.year, datetime.now().year + 1))
    return const.PERIOD_MAP


def unzip(path):
    if not path.endswith(".zip"):
        return path
    with zipfile.ZipFile(path, "r") as zip_ref:
        new_path = path.split(".zip")[0]
        zip_ref.extractall()
        return new_path


def read_json(file) -> Union[Dict, List]:
    with open(file) as f:
        return json.load(f)


def dump_to_json(data=None, file=None):
    with open(file, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


def to_stdout(path, data):
    if path == "json":
        return data.to_json()
    return data.to_csv()


def basedir_exists(path):
    if not os.path.isdir(os.path.dirname(path)):
        return False
    return True


def rewrite(path):
    if os.path.exists(path):
        logging.warning("File already exist!")
        answer = input(f"Overwrite {path}? (y/n)")
        if answer == "y":
            return True
        else:
            return False
    return True


def df_to_file(path, data):
    if path is None or path in ("csv", "json"):
        return to_stdout(path, data)

    if not basedir_exists(path):
        return f"Directory does not exist: `{os.path.dirname(path)}`"

    if not rewrite(path):
        return ""

    if path.endswith(".csv"):
        data.to_csv(path)
    elif path.endswith(".json"):
        data.to_json(path)
    return f"Data was written to {path}"


def ts_to_date(date):
    # Note: not too robust.
    if date > time.time() + const.HUNDRED_YEARS_IN_SECONDS:
        date /= 1000
    return datetime.fromtimestamp(date)


def dt(y: int = 2004, m: int = 1, d: int = 1, h: int = 0, **kwargs):
    return datetime(year=y, month=m, day=d, hour=h, **kwargs)


def get_start_based_on_period(join_date, period):
    if period == "y":
        return datetime(join_date.year, 1, 1)
    elif period == "m":
        return datetime(join_date.year, join_date.month, 1)
    return join_date


def prefill_dict(dict, keys, value):
    for k in keys:
        dict[k] = copy.copy(value)
    return dict


def fill_dict(dictionary, key, value):
    if dictionary.get(key) is not None:
        dictionary[key] += value
    else:
        dictionary[key] = value
    return dictionary


def sort_dict(dictionary, func=lambda x: x, reverse=False):
    return {
        key: value
        for key, value in sorted(dictionary.items(), key=func, reverse=reverse)
    }


def remove_items_where_value_is_falsible(dictionary):
    return {k: v for k, v in dictionary.items() if v}


def slice_dict(dictionary, n):
    return dict(islice(dictionary.items(), n))


def unify_dict_keys(first, second):
    for key in first.keys():
        if second.get(key) is None:
            second[key] = 0
    for key in second.keys():
        if first.get(key) is None:
            first[key] = 0
    return first, second


def get_parent_directory_of_file(root, files, extension, contains_string) -> str:
    for file_name in files:
        if (
            file_name.endswith(extension)
            and contains_string is not None
            and contains_string in file_name
        ):
            return root


def get_all_jsons(root, files, extension, contains_string) -> List[str]:
    paths = []
    for file_name in files:
        if (
            file_name.endswith(extension)
            and contains_string is not None
            and contains_string in file_name
        ):
            paths.append(os.path.join(root, file_name))
    return paths


def walk_directory_and_search(path, func, extension, contains_string=""):
    paths = []
    for root, _, files in os.walk(path):
        res = func(root, files, extension, contains_string)
        if isinstance(res, list):
            paths += res
        elif isinstance(res, str):
            paths.append(res)
    for path in paths:
        yield path


def dir_stripped(obj):
    return [x for x in dir(obj) if not x.startswith("_")]


def is_nan(value) -> bool:
    return not isinstance(value, str) and math.isnan(value)


def emoji_matcher(text):
    regex_pattern = re.compile(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    return re.findall(regex_pattern, text)


def replace_accents(string):
    for char in const.ACCENTS_MAP.keys():
        if char in string:
            string = string.replace(char, const.ACCENTS_MAP[char])
    return string


def utf8_decoder(string):
    return string.encode("latin_1").decode("utf-8")


def decode_data(
    obj: Union[str, List, Dict], decoder: Callable,
):
    if isinstance(obj, str):
        return decoder(obj)

    if isinstance(obj, list):
        return [decode_data(o, decoder) for o in obj]

    if isinstance(obj, dict):
        return {key: decode_data(item, decoder) for key, item in obj.items()}

    return obj


# dataframe utils
def stack_dfs(*args, sort=True):
    if not sort:
        return pd.concat(args)
    return pd.concat(args).sort_index()


@decorators.start_end_period_checker
def filter_by_date(df: pd.DataFrame, start=None, end=None, period=None):
    """
    @param df:
    @param start: datetime object or date string with format `YYYY-MM-DD`
    @param end: datetime object or date string with format `YYYY-MM-DD`
    @param period: one of {y|m|d|h}
    @return:
    """
    if not len(df):
        return df
    if start and end:
        return df.loc[start:end]
    elif start and not end and not period:
        return df.loc[start:]
    elif end and not start and not period:
        return df.loc[:end]
    elif start and period and not end:
        return df.loc[start : start + period]
    elif not start and period and end:
        return df.loc[end - period : end]


@decorators.column_checker
@decorators.string_kwarg_to_list_converter("channels")
def filter_by_channel(
    df: pd.DataFrame, column: str = "partner", channels: Union[str, List[str]] = None
):
    if not channels or not len(df):
        return df
    return handle_filter_df(df, column, channels)


@decorators.column_checker
@decorators.string_kwarg_to_list_converter("senders")
def filter_by_sender(
    df: pd.DataFrame,
    column: str = "sender_name",
    senders: Union[str, List[str]] = None,
    me: str = None,
):
    if not senders or not len(df):
        return df
    if senders == ["me"]:
        return df[df[column] == me]
    elif senders == ["partner"]:
        return df[df[column] != me]
    elif senders:
        return handle_filter_df(df, column, senders)


def handle_filter_df(df, column, filter_params):
    match = df[df[column].isin(filter_params)]
    if match is None or len(match) == 0:
        logging.warning(
            f"None of the filter parameters ({filter_params}) you specified exist in this df's `{column}` column."
        )
        return df[0:0]
    return match


def filer_empty_cols(df: pd.DataFrame):
    empty_cols = [col for col in df.columns if df[col].isnull().all()]
    if len(df) and len(df.columns):
        df.drop(empty_cols, axis=1, inplace=True)
    return df


@decorators.start_end_period_checker
def generate_date_series(join_date, period="y", start=None, end=None):
    dates = []
    start = start or get_start_based_on_period(join_date, period)
    end = end or datetime.now()

    intermediate = start
    while intermediate <= end:  # means that we want to have the end in it as well
        dates.append(intermediate)
        intermediate = intermediate + const.DELTA_MAP.get(period)
    return dates
