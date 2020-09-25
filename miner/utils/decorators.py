import os
from datetime import datetime

from miner.utils import const, utils


class string_kwarg_to_list_converter:
    def __init__(self, kw_arg):
        self.kw_arg = kw_arg

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            value = kwargs.get(self.kw_arg)
            if not value:
                return func(*args, **kwargs)
            if isinstance(value, str):
                kwargs[self.kw_arg] = value.split(";!;") if ";!;" in value else [value]
            if isinstance(value, tuple):
                kwargs[self.kw_arg] = list(value)
            if not isinstance(kwargs[self.kw_arg], list):
                raise ValueError(
                    f"Parameter `{self.kw_arg}` should be type of Union[str, List[str]], got: {type(kwargs[self.kw_arg])}"
                )
            return func(*args, **kwargs)

        return wrapper


def path_exists(func):
    def wrapper(*args):
        path = args[0]
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"`{path}` doe snot exist. You must specify a valid path."
            )
        return func(*args)

    return wrapper


def outputter(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if not len(res):
            return
        return utils.df_to_file(kwargs.get("output"), res)

    return wrapper


def kind_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get("kind") in ("private", "group"):
            raise ValueError(
                f"{kwargs.get('kind')} has to be either `private` or `group`!"
            )
        return func(*args, **kwargs)

    return wrapper


def column_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get("column") or not isinstance(kwargs.get("column"), str):
            raise ValueError(
                f'Parameter `column` should be type of str, got: {type(kwargs["column"])}'
            )
        return func(*args, **kwargs)

    return wrapper


def period_checker(func):
    def wrapper(*args, **kwargs):
        if (
            not kwargs.get("period")
            or const.DELTA_MAP.get(kwargs.get("period")) is None
        ):
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


def start_end_period_checker(func):
    def wrapper(*args, **kwargs):
        if kwargs.get("start") is None and kwargs.get("end") is None:
            kwargs["start"] = const.FACEBOOK_FOUNDATION_DATE
            kwargs["end"] = datetime.now()
            return func(*args, **kwargs)

        if kwargs.get("start") and isinstance(kwargs.get("start"), str):
            kwargs["start"] = datetime.strptime(kwargs.get("start"), const.DATE_FORMAT)
        if kwargs.get("end") and isinstance(kwargs.get("end"), str):
            kwargs["end"] = datetime.strptime(kwargs.get("end"), const.DATE_FORMAT)

        if kwargs.get("period"):
            if const.DELTA_MAP[kwargs.get("period")] is None:
                raise ValueError("Parameter `period` should be one of {y|m|d|h}")
            kwargs["period"] = const.DELTA_MAP[kwargs.get("period")]

        return func(*args, **kwargs)

    return wrapper
