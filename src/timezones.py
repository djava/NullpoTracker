''' Sets up timezone alignment for the modification
    time versus the current time on the replay files
    for NullpoTracker
'''

import datetime
import configparser
import globalVars

US_DST_START = datetime.datetime(datetime.datetime.now().year, 3, 8, 2)
US_DST_END = datetime.datetime(datetime.datetime.now().year, 11, 1, 2)
CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

TIMEZONE_NAME = CONFIG['TIMEZONE']['timezone']
USE_DST = CONFIG['TIMEZONE']['USE_DST'].lower() == 'true'

UTC_OFFSET_DICT = {
    'ATH':  2, 'PAR':  1, 'UTC':  0,
    'BRZ': -3, 'ATL': -4, 'EST': -5,
    'CST': -6, 'MST': -7, 'PST': -8,
    'AK': -9, 'HW': -10
}


class timezone(datetime.tzinfo):
    def __init__(self, timezoneName: str, dst: bool):
        global UTC_OFFSET_DICT

        self._timezoneName = timezoneName
        self.stdoffset = datetime.timedelta(
            hours=UTC_OFFSET_DICT[timezoneName])
        self.usesDST = dst

    def utcoffset(self, dt: datetime.datetime) -> datetime.time:
        return -self.stdoffset - self.dst(dt)

    def dst(self, dt: datetime) -> datetime.timedelta:
        global US_DST_START, US_DST_END

        dt = dt.replace(tzinfo=None)

        if self.usesDST and dt >= US_DST_START and dt <= US_DST_END:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def name(self) -> str:
        return _timezoneName


UTC = timezone('UTC', False)
CURRENT_TIMEZONE = timezone(TIMEZONE_NAME, USE_DST)