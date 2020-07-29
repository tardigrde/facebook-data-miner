import json

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
          'november', 'december']


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


def read_json(file):
    with open(file) as f:
        return json.load(f)


def dump_to_json(data=None, file=None):
    with open(file, 'w') as f:
        json.dump(data, f)


def decode_text(obj):
    if isinstance(obj, str):
        return obj.encode('latin_1').decode('utf-8')

    if isinstance(obj, list):
        return [decode_text(o) for o in obj]

    if isinstance(obj, dict):
        return {key: decode_text(item) for key, item in obj.items()}

    return obj


def order_list_of_dicts(lst, key='timestamp_ms'):
    return sorted(lst, key=lambda k: k[key])


accents_map = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ö": "o",
    "ő": "o",
    "ú": "u",
    "ü": "u",
    "ű": "u",
    # "Á": "A",
    # "É": "E",
    # "Í": "I",
    # "Ó": "O",
    # "Ö": "O",
    # "Ő": "O",
    # "Ú": "U",
    # "Ü": "U",
    # "Ű": "U",
}


def year_and_month_checker(func):
    """
    Higher-order function for checking if specified @year passed to @func is in the data dict.
    @param func:
    @return:
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        stats = args[1]
        year = kwargs.get('year')
        month = kwargs.get('month')

        if year is not None and not isinstance(year, int):
            kwargs['year'] = int(year)
            year = kwargs.get('year')

        if year is None and month is None:
            return func(*args, **kwargs)

        if year and stats.get('grouped').get(year) is None:
            #print(f"{year} is not in the data dict.")
            return 0
        elif year and month and stats.get('grouped').get(year).get(month) is None:
            #print(f"{year}/{month} is not in the data dict.")
            return 0
        return func(*args, **kwargs)

    return wrapper


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
