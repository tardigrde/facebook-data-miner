from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta

# https://en.wikipedia.org/wiki/ISO_8601
DATE_FORMAT = "%Y-%m-%d"
HUNDRED_YEARS_IN_SECONDS = 100 * 365 * 24 * 60 * 60
FACEBOOK_FOUNDATION_DATE = datetime(year=2004, month=2, day=4, tzinfo=pytz.UTC)

MESSAGE_SUBPATH = "messages/inbox"
MEDIA_DIRS = ["photos", "gifs", "files", "videos", "audio_files"]

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
    "y": None,
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

HUMAN_READABLE_PERIODS = {
    "y": "Yearly",
    "m": "Monthly",
    "d": "Daily",
    "h": "Hourly",
}
