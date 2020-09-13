import math
import copy
from typing import Union, List, Dict, Callable, Any, NamedTuple
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import dateparser
from itertools import islice
import json
import os
import time
import pandas as pd
import re

# https://en.wikipedia.org/wiki/ISO_8601
DATE_FORMAT = "%Y-%m-%d"
HUNDRED_YEARS_IN_SECONDS = 100 * 365 * 24 * 60 * 60
FACEBOOK_FOUNDATION_DATE = datetime(year=2004, month=2, day=4)
# TODO: get this from somewhere
ME = "Levente Csőke"
JOIN_DATE = datetime(year=2009, month=10, day=2)
MESSAGE_SUBPATH = "messages/inbox"
MEDIA_DIRS = ["photos", "gifs", "files", "videos", "audio"]
MONTHS = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
]
WEEKDAYS = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]
PERIOD_MAP = {
    "y": list(range(JOIN_DATE.year, datetime.now().year + 1)),
    "m": MONTHS,
    "d": WEEKDAYS,
    "h": list(range(24)),
}
DELTA_MAP = {
    "y": relativedelta(years=+1),
    "m": relativedelta(months=+1),
    "d": timedelta(days=1),
    "h": timedelta(hours=1),
}
ACCENTS_MAP = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ö": "o",
    "ő": "o",
    "ú": "u",
    "ü": "u",
    "ű": "u",
}

MESSAGE_TYPE_MAP = {"private": "Regular", "group": "RegularGroup"}
STAT_MAP = {
    "mc": "Message",
    "text_mc": "Text message",
    "media_mc": "Media message",
    "wc": "Word",
    "cc": "Character",
}
# TODO: get this from somewhere
ME = "Levente Csőke"
JOIN_DATE = datetime(year=2009, month=10, day=2)


class CommandChainCreator:
    def __init__(self):
        self.commands = []

    def __call__(self, data: Any) -> Any:
        for cmd in self.commands:
            data = cmd(data)
        return data

    def register_command(self, func, *args, **kwargs):
        cmd = Command(func, *args, **kwargs)
        self.commands.append(cmd)


class Command:
    def __init__(self, cmd, *args, **kwargs):
        self._cmd = cmd
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *args):
        return self._cmd(*(args + self._args), **self._kwargs)


class TooFewPeopleError(Exception):
    pass


def get_group_convo_map(data):
    group_convo_map = {}
    # no need for prefill
    # group_convo_map = utils.prefill_dict(
    #     group_convo_map, list(self._private.keys()), []
    # )
    for channel, convo in data.items():
        for participant in convo.metadata.participants:
            # p: 2 participants
            # g: 2+ participants
            group_convo_map = fill_dict(group_convo_map, participant, [channel])
            group_convo_map[participant] = list(
                set(group_convo_map.get(participant))
            )  # just making sure there is no duplicate, so I don't have to go over it again later
    return group_convo_map


class string_kwarg_to_list_converter:
    def __init__(self, kw_arg):
        self.kw_arg = kw_arg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            value = kwargs.get(self.kw_arg)
            if not value:
                return func(*args, **kwargs)
            if isinstance(value, str):
                kwargs[self.kw_arg] = [value]
            if not isinstance(kwargs[self.kw_arg], list):
                raise ValueError(
                    f"Parameter `{self.kw_arg}` should be type of Union[str, List[str]], got: {type(kwargs[self.kw_arg])}"
                )
            return func(*args, **kwargs)

        return wrapper


def column_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get("column") or not isinstance(kwargs.get("column"), str):
            raise ValueError(
                f'Parameter `column` should be type of pd.Series, got: {type(kwargs["column"])}'
            )
        return func(*args, **kwargs)

    return wrapper


def period_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get("period") or DELTA_MAP[kwargs.get("period")] is None:
            raise ValueError("Parameter `period` should be one of {y, m, d, h}")
        return func(*args, **kwargs)

    return wrapper


def attribute_checker(func):
    def wrapper(*args, **kwargs):
        statistic = kwargs.get("statistic")
        if not statistic or statistic not in ("mc", "wc", "cc"):
            raise ValueError("Parameter `statistic` should be one of {mc, wc, cc}")
        return func(*args, **kwargs)

    return wrapper


# TODO support adding only start or end
def start_end_period_checker(func):
    def wrapper(*args, **kwargs):
        if kwargs.get("start") is not None and kwargs.get("end") is not None:
            return func(*args, **kwargs)

        if kwargs.get("start") is None and kwargs.get("end") is None:
            kwargs["start"] = FACEBOOK_FOUNDATION_DATE
            kwargs["end"] = datetime.now()
            return func(*args, **kwargs)

        if not kwargs.get("period") or DELTA_MAP[kwargs.get("period")] is None:
            raise ValueError("Parameter `period` should be one of {y|m|d|h}")
        kwargs["period"] = DELTA_MAP[kwargs.get("period")]
        return func(*args, **kwargs)

    return wrapper


def read_json(file) -> Union[Dict, List]:
    with open(file) as f:
        return json.load(f)


def dump_to_json(data=None, file=None):
    with open(file, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)


def ts_to_date(date):
    # Note: not too robust.
    if date > time.time() + HUNDRED_YEARS_IN_SECONDS:
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


def get_stats_for_time_intervals(stat_getter, time_series, period, subject="all"):
    data = {}
    for i in range(len(time_series)):
        start = time_series[i]
        try:  # with this solution we will have data for the very last moments until datetime.now()
            end = time_series[i + 1]
        except IndexError:
            end = None
        data[start] = stat_getter.filter(
            subject=subject, start=start, end=end, period=period
        )
    return data


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
    for char in ACCENTS_MAP.keys():
        if char in string:
            string = string.replace(char, ACCENTS_MAP[char])
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


@start_end_period_checker
def filter_by_date(df: pd.DataFrame, start=None, end=None, period=None):
    """
    @param df:
    @param start: datetime object or date string with format `YYYY-MM-DD`
    @param end: datetime object or date string with format `YYYY-MM-DD`
    @param period: one of {y|m|d|h}
    @return:
    """
    if start and end:
        return df.loc[start:end]
    elif start and not end:
        return df.loc[start : start + period]
    elif not start and end:
        return df.loc[end - period : end]


@column_checker
@string_kwarg_to_list_converter("channels")
def filter_by_channel(
    df: pd.DataFrame, column: str = "partner", channels: Union[str, List[str]] = None
):
    if not channels:
        return df
    partner_matched = df[df[column].isin(channels)]
    return partner_matched


@column_checker
@string_kwarg_to_list_converter("senders")
def filter_by_sender(
    df: pd.DataFrame, column: str = "sender_name", senders: Union[str, List[str]] = None
):
    if not senders:
        return df
    partner_matched = df[df[column].isin(senders)]
    return partner_matched


@column_checker
def filter_for_subject(df: pd.DataFrame, column: str = "", subject: str = "all"):
    if subject == "me":
        return df[df[column] == ME]
    elif subject == "partner":
        return df[df[column] != ME]
    elif subject and subject != "all":
        return df[df[column] == subject]
    return df


@start_end_period_checker
def generate_date_series(period="y", start=None, end=None):
    dates = []
    join_date = JOIN_DATE
    start = start or get_start_based_on_period(join_date, period)
    end = end or datetime.now()

    intermediate = start
    while intermediate <= end:  # means that we want to have the end in it as well
        dates.append(intermediate)
        intermediate = intermediate + DELTA_MAP.get(period)
    return dates


class PeriodManager:
    # TODO clear this class up
    #  maybe subclasses? do we need it?
    @staticmethod
    def set_df_grouping_indices_to_datetime(df, period):
        datetimes = []
        for index, row in df.iterrows():
            key = PERIOD_MANAGER.ordinal_to_datetime(period, index)
            datetimes.append(key)

        df["timestamp"] = datetimes
        return df.set_index("timestamp", drop=True)

    @staticmethod
    def get_grouping_rules(period, df):
        if period == "y":
            return [df.index.year]
        if period == "m":
            return [df.index.year, df.index.month]
        if period == "d":
            return [df.index.year, df.index.month, df.index.day]
        if period == "h":
            return [df.index.year, df.index.month, df.index.day, df.index.hour]

    @staticmethod
    def ordinal_to_datetime(period, index):
        if period == "y":
            return datetime(year=index, month=1, day=1)
        if period == "m":
            return datetime(year=index[0], month=index[1], day=1)
        if period == "d":
            return datetime(*index)
        if period == "h":
            return datetime(*index)

    @staticmethod
    def date_to_period(date, period):
        if period == "y":
            return date.year
        if period == "m":
            return MONTHS[date.month - 1]
        if period == "d":
            return WEEKDAYS[date.weekday()]
        if period == "h":
            return date.hour

    @staticmethod
    def sorting_method(period):
        if period == "y":
            return lambda x: x
        if period == "m":
            return lambda x: MONTHS.index(x[0])
        if period == "d":
            return lambda x: WEEKDAYS.index(x[0])
        if period == "h":
            return lambda x: x

    @staticmethod
    def delta(period):
        if period == "y":
            return relativedelta(years=+1)
        if period == "m":
            return relativedelta(months=+1)
        if period == "d":
            return timedelta(days=1)
        if period == "h":
            return timedelta(hours=1)


PERIOD_MANAGER = PeriodManager()

#################################################
