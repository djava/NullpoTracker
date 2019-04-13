import datetime
import configparser

NOW = datetime.datetime.now()
US_DST_START = datetime.datetime(NOW.year, 3, 8, 2)
US_DST_END = datetime.datetime(NOW.year, 11, 1, 2)
CONFIG = configparser.ConfigParser()
CONFIG.read('./config.ini')

TIMEZONE_NAME = CONFIG['TIMEZONE']['timezone']
USE_DST = CONFIG['TIMEZONE']['USE_DST']

UTC_OFFSET_DICT = {
    'ATH': 2,
    'PAR': 1,
    'UTC': 0,
    'BRZ': -3,
    'ATL': -4,
    'EST': -5,
    'CST': -6,
    'MST': -7,
    'PST': -8,
    'AK': -9,
    'HW': -10,
}


class timezone(datetime.tzinfo):

    def __init__(self):
        global USE_DST, UTC_OFFSET_DICT, TIMEZONE_NAME

        self.stdoffset = datetime.timedelta(
            hours=UTC_OFFSET_DICT[TIMEZONE_NAME])
        self.usesDST = USE_DST

    def utcoffset(self, dt):
        return -self.stdoffset - self.dst(dt)

    def dst(self, dt):
        global US_DST_START, US_DST_END

        dt = dt.replace(tzinfo=None)

        if self.usesDST:
            if dt >= US_DST_START and dt <= US_DST_END:
                return datetime.timedelta(hours=1)
            else:
                return datetime.timedelta(0)
        else:
            return datetime.timedelta(0)


class UTC_TIMEZONE(timezone):
    def __init__(self):
        self.stdoffset = datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

UTC = UTC_TIMEZONE()
CURRENT_TIMEZONE = timezone()
