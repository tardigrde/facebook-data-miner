from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from miner.utils import const


# NOTE this class is a little bit to verbose
class PeriodManager:
    @staticmethod
    def set_df_grouping_indices_to_datetime(df, timeframe):
        datetimes = []
        for index, row in df.iterrows():
            key = PERIOD_MANAGER.ordinal_to_datetime(timeframe, index)
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
            return const.MONTHS[date.month - 1]
        if period == "d":
            return const.WEEKDAYS[date.weekday()]
        if period == "h":
            return date.hour

    @staticmethod
    def sorting_method(period):
        if period == "y":
            return lambda x: x
        if period == "m":
            return lambda x: const.MONTHS.index(x[0])
        if period == "d":
            return lambda x: const.WEEKDAYS.index(x[0])
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
