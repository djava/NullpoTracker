import configparser
import datetime
import timezones
import pickle
import enum

# Config.ini file
CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

# Path of the nullpomino replay folder
REPLAY_PATH = CONFIG['SETUP']['nullpoPath'] + '/replay/'

# Tracks the time NullpoTracker was opened, mostly just to check if
# the ignore files have changed since it was last opened
OPEN_TIME = datetime.datetime.now(tz=timezones.CURRENT_TIMEZONE)
with open('lastTimeOpenedDT.pickle', 'rb+') as lTO:
    try:
        LAST_TIME_OPENED = pickle.load(lTO)
    except Exception:
        # Just sets it to the epoch if the .pickle
        # file is empty or corrupted, not a big deal
        # if the ignores run extraneously
        LAST_TIME_OPENED = datetime.datetime(1970, 1, 1, tzinfo=timezones.UTC)

    pickle.dump(OPEN_TIME, lTO, pickle.HIGHEST_PROTOCOL)
