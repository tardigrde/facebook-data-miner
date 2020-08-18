from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import dateparser
from itertools import islice
import json
import os
import pandas as pd

MESSAGE_SUBPATH = 'messages/inbox'
MEDIA_DIRS = ['photos', 'gifs', 'files', 'videos', 'audio']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
          'november', 'december']
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
PERIOD_MAP = {
    'y': None,
    'm': MONTHS,
    'd': WEEKDAYS,
    'h': None,
}
DELTA_MAP = {
    'y': relativedelta(years=+1),
    'm': relativedelta(months=+1),
    'd': timedelta(days=1),
    'h': timedelta(hours=1)
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


def ts_to_date(date):
    return datetime.fromtimestamp(date / 1000)


def read_json(file):
    with open(file) as f:
        return json.load(f)


def dump_to_json(data=None, file=None):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def order_list_of_dicts(lst, key='timestamp_ms'):
    return sorted(lst, key=lambda k: k[key])


def year_converter(func):
    """
    Higher-order function that converts @year param passed to @func into numeric version.
    @param func:
    @return:
    """

    def wrapper(*args, **kwargs):
        if not kwargs.get('year'):
            return func(*args, **kwargs)
        if not isinstance(kwargs.get('year'), int):
            if kwargs.get('year').isdigit():
                kwargs['year'] = int(kwargs.get('year'))
            else:
                print(f'Year is not a digit. Given year: {kwargs.get("year")}')
        return func(*args, **kwargs)

    return wrapper


def month_converter(func):
    """
    Higher-order function that converts @month param passed to @func into numeric version.
    @param func:
    @return:
    """

    def wrapper(*args, **kwargs):
        if not kwargs.get('month'):
            return func(*args, **kwargs)
        if isinstance(kwargs['month'], str) and not kwargs['month'].isdigit():
            kwargs['month'] = MONTHS.index(kwargs['month'].lower()) + 1
        return func(*args, **kwargs)

    return wrapper


def subject_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get('subject') or kwargs.get('subject') not in ('all', 'me', 'partner'):
            raise ValueError('Parameter `subject` should be one of {all, me, partner}')
        return func(*args, **kwargs)

    return wrapper


def date_checker(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('start') is not None and isinstance(kwargs.get('start'), str):
            kwargs['start'] = dateparser.parse(kwargs.get('start'))
        if kwargs.get('end') is not None and isinstance(kwargs.get('end'), str):
            kwargs['end'] = dateparser.parse(kwargs.get('end'))
        if kwargs.get('start') is None and kwargs.get('end') is None:
            kwargs['start'] = datetime(year=2006, month=1, day=1)  # foundation date of Facebook
            kwargs['end'] = datetime.now()
        if sum(map(bool, [kwargs.get('start'), kwargs.get('end'), kwargs.get('period')])) < 2:
            raise ValueError(
                'At least two of the following three input variables has to be passed: {start, end, period}')
        return func(*args, **kwargs)

    return wrapper


def start_end_period_checker(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('start') is not None and kwargs.get('end') is not None:
            return func(*args, **kwargs)
        if not kwargs.get('period') or DELTA_MAP[kwargs.get('period')] is None:
            raise ValueError('Parameter `period` should be one of {y, m, d, h}')
        kwargs['period'] = DELTA_MAP[kwargs.get('period')]
        return func(*args, **kwargs)

    return wrapper


def period_checker(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get('period') or DELTA_MAP[kwargs.get('period')] is None:
            raise ValueError('Parameter `period` should be one of {y, m, d, h}')
        return func(*args, **kwargs)

    return wrapper


def get_start_based_on_period(join_date, period):
    if period == 'y':
        return datetime(join_date.year, 1, 1)
    elif period == 'm':
        return datetime(join_date.year, join_date.month, 1)
    return join_date


@period_checker
def generate_date_series(period='y', start=None, end=None):
    dates = []

    join_date = datetime(year=2009, month=10, day=2)  # TODO later get this from somewhere
    start = start or get_start_based_on_period(join_date, period)
    end = end or datetime.now()

    intermediate = start
    while intermediate <= end:  # means that we want to have the end in it as well
        dates.append(intermediate)
        intermediate = intermediate + DELTA_MAP.get(period)
    return dates


def dt(year: int = 2004, month: int = 1, day: int = 1, hour: int = 0):
    return datetime(year=year, month=month, day=day, hour=hour)


def get_messages(*files, decode=True):
    data = {}
    for file in files:
        temp = decode_text(read_json(file)) if decode else read_json(file)
        if not data:
            data = temp
        elif data.get('messages') and temp.get('messages'):
            data['messages'] += temp.get('messages')
            if sorted(temp.keys()) != sorted(data.keys()):
                data = {**temp, **data}
    return data


def decode_text(obj):
    if isinstance(obj, str):
        return obj.encode('latin_1').decode('utf-8')

    if isinstance(obj, list):
        return [decode_text(o) for o in obj]

    if isinstance(obj, dict):
        return {key: decode_text(item) for key, item in obj.items()}

    return obj


def get_dataframe(data, field=None):
    data = data.get(field) if field else data
    return pd.DataFrame(data)


def lower_names(col):
    return col.str.lower()


def replace_accents(text):
    for char in ACCENTS_MAP.keys():
        if char in text:
            text = text.replace(char, ACCENTS_MAP[char])
    return text.replace(' ', '')


def without_accent_and_whitespace(col):
    return col.apply(replace_accents)


def walk_directory_and_search(path, extension, contains_string=None):
    paths = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(extension):
                if contains_string is not None and contains_string in file_name:
                    paths.append(os.path.join(root, file_name))
    return paths


def fill_dict(dictionary, key, value):
    if dictionary.get(key) is not None:
        dictionary[key] += value
    else:
        dictionary[key] = value
    return dictionary


def month_sorter(x):
    return MONTHS.index(x[0])


def count_stat_for_period(data, period):
    # TODO sort by lists
    periods = {}
    for key, value in data.items():
        if period == 'y':
            periods = fill_dict(periods, key.year, value)
            periods = dict(sorted(periods.items()))
        elif period == 'm':
            periods = fill_dict(periods, MONTHS[key.month - 1], value)
            periods = dict(sorted(periods.items(), key=lambda x: MONTHS.index(x[0])))
        elif period == 'd':
            periods = fill_dict(periods, WEEKDAYS[key.weekday()], value)
            periods = dict(sorted(periods.items(), key=lambda x: WEEKDAYS.index(x[0])))
        elif period == 'h':
            periods = fill_dict(periods, key.hour, value)
            periods = dict(sorted(periods.items()))
    return periods


def sort_dict(dictionary, func=lambda x: x, reverse=False):
    return {key: value for key, value in sorted(dictionary.items(), key=func, reverse=reverse)}


def remove_items_where_value_is_falsible(dictionary):
    return {k: v for k, v in dictionary.items() if v}


# keep only first 20 entries
def slice_dict(dictionary, n):
    return dict(islice(dictionary.items(), n))


def attribute_checker(func):
    def wrapper(*args, **kwargs):
        statistic = kwargs.get('statistic')
        if not statistic or statistic not in ('msg_count', 'word_count', 'char_count'):
            raise ValueError('Parameter `statistic` should be one of {msg_count, word_count, char_count}')
        return func(*args, **kwargs)

    return wrapper
