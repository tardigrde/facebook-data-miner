import os
import json
import pandas as pd
import dateparser
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

MESSAGE_SUBPATH = 'messages/inbox'
MEDIA_DIRS = ['photos', 'gifs', 'files', 'videos', 'audio']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
          'november', 'december']
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


def read_json(file):
    with open(file) as f:
        return json.load(f)


def dump_to_json(data=None, file=None):
    with open(file, 'w') as f:
        json.dump(data, f)


def order_list_of_dicts(lst, key='timestamp_ms'):
    return sorted(lst, key=lambda k: k[key])


#


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


def period_checker(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('start') is not None and kwargs.get('end') is not None:
            return func(*args, **kwargs)

        if not kwargs.get('period') or DELTA_MAP[kwargs.get('period')] is None:
            raise ValueError('Parameter `period` should be one of {y, m, d, h}')
        kwargs['period'] = DELTA_MAP[kwargs.get('period')]
        return func(*args, **kwargs)

    return wrapper


def generate_date_series(start=None, end=None, period=None):
    if period is None or DELTA_MAP.get(period) is None:
        raise ValueError('Parameter `period` should be one of {y, m, d, h}')
    start = start or datetime(year=2009, month=10, day=2, hour=0)  # TODO LATER change this to date when user joined FB
    end = end or datetime.now()

    dates = []
    intermediate = start
    while intermediate <= end:
        dates.append(intermediate)
        intermediate = intermediate + DELTA_MAP.get(period)
    return dates


def get_stats_for_intervals(func, df, time_series, subject='all'):
    data = {}
    for i in range(len(time_series) - 1):  # only looping len - 1 times
        start = time_series[i]
        # TODO test it with new data injected/modified at runtime <- this is hard
        # what is this about actually?
        end = time_series[i + 1]
        data[start] = func(df, subject=subject, start=start, end=end)
    return data


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


def lower_names(col):
    return col.str.lower()


def replace_accents(text):
    for char in ACCENTS_MAP.keys():
        if char in text:
            text = text.replace(char, ACCENTS_MAP[char])
    return text.replace(' ', '')


def without_accent_and_whitespace(col):
    return col.apply(replace_accents)


def walk_directory_and_search(path, extension):
    paths = []
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith(extension):
                paths.append(os.path.join(root, file_name))
    return paths
