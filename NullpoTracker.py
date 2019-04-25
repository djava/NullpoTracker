# For detecting the active window
from win32 import win32gui
from win32 import win32process

# For aligning the time modififed with the current time
from timezones import CURRENT_TIMEZONE as TIMEZONE
from timezones import UTC

# For time comparisons
import time
import datetime

# For use of non-.py files
import sqlite3
import configparser
import pickle

# For various use and parsing and stuff
import os
import re


# Database for tracked games
DB = sqlite3.connect('./NullpoTracker.db')

# Config.ini file
CONFIG = configparser.ConfigParser()
CONFIG.read('./config.ini')

# Path of the nullpomino replay folder
REPLAY_PATH = CONFIG['SETUP']['nullpoPath'] + '/replay/'

# These files let you make the tracker to ignore some of the files
with open('./ignoreReps.txt') as ignoreReps:
    IGNORE_REPS = ignoreReps.read().split('\n')
with open('./ignoreModes.txt') as ignoreModes:
    IGNORE_MODES = ignoreModes.read().split('\n')

# Tracks the time NullpoTracker was opened, mostly just to check if
# the ignore files have changed since it was last opened
OPEN_TIME = datetime.datetime.now(tz=TIMEZONE)
with open('./lastTimeOpenedDT.pickle', 'rb') as lTO:
    try:
        LAST_TIME_OPENED = pickle.load(lTO)
    except EOFError:
        # Just sets it to the epoch if the .pickle
        # file is empty or corrupted, not a big deal
        # if the ignores run extraneously
        LAST_TIME_OPENED = datetime.datetime(1970, 1, 1)
with open('lastTimeOpenedDT.pickle', 'wb') as lTO:
    pickle.dump(OPEN_TIME, lTO, pickle.HIGHEST_PROTOCOL)


def modTime(path, *includeReplayPath):
    ''' Returns the last modified time of a file

        Path is the path of the file to modTime

        Set includeReplayPath to True to just add the replay
        path to the arg to shorten function calls

        For  a file's modified time, os always returns it in seconds
        since the epoch, so we have to add the getmtime call as a
        timedelta in seconds after Jan 1 1970

        Tzinfo always has to be set to UTC because it doesn't let
        you compare datetimes if one has a timezone and the other
        doesn't.  Also, os returns it in UTC so you'd have to add
        it anyway for accurate comparisons.
    '''

    global REPLAY_PATH, UTC

    return datetime.datetime(1970, 1, 1, tzinfo=UTC) + datetime.timedelta(
                seconds=os.path.getmtime(
                        (REPLAY_PATH + path) if includeReplayPath else path))


def checkAndHandleIgnores():
    ''' Removes the values for each file and mode in the ignore files.
        Also sets the ignored values in those files to true in the DB.
    '''

    global LAST_TIME_OPENED, IGNORE_MODES, IGNORE_REPS, DB

    # modIgnoreReps is True if ignoreReps was changes
    # since the last time NullpoTracker was run, to know
    # if it has to update the db for new reps to ignore
    modIgnoreReps = modTime(
        './ignoreReps.txt') > LAST_TIME_OPENED

    if modIgnoreReps:
        # Removes all the values for every  file in ignoreReps
        for rep in IGNORE_REPS:
            DB.execute(f"UPDATE GamesTracked\
                        SET time=NULL,\
                            PPS=NULL,\
                            mode=NULL,\
                            score=NULL,\
                            ignore=1\
                        WHERE fileName='{rep}';")

    if IGNORE_MODES != ['']:
        for mode in IGNORE_MODES:
            DB.execute(f'UPDATE GamesTracked\
                       SET time=NULL,\
                       PPS=NULL,\
                       mode=NULL,\
                       score=NULL,\
                       ignore=1\
                       WHERE mode="{mode}";')

    DB.commit()


def isNullpo():
    ''' Returns true if the current active window is Nullpo,
        false if it's not

        Only works on Windows

        Gets the PID for the current active window as currentPid
        Compares that against a dictionary of parsed tasklist data
        If currentPid is the same as the pid for javaw.exe (Nullpo),
        it will return True

        Will produce a false positive if you use other applications
        that run as javaw.exe, IDK how to fix that, but it's not a
        big deal if it does because it'll just do nothing if the
        replays folder hasn't changed. It'll be a little costly
        when the program that false-positives closes but no biggie.
    '''
    #            |------Converts a HWND to a PID------|
    currentPid = win32process.GetWindowThreadProcessId(
        # |-Gets HWND of active window-|
        win32gui.GetForegroundWindow())[1]

    #          Splits each line in tasklist into just the PID and name.
    #          It has the [::-1] to make it prettier on the dict comp.
    tasklist = [re.split(r' {3,}| Services| Console', i)[:2][::-1]
                # Gets the output of running tasklist, and splits it by line.
                # Lines 0-2 are garbage, last line is blank.
                for i in os.popen('tasklist').read().split('\n')[3:-1]]

    # Converts the PID and name into a dict to find Nullpo more easily
    tasklist = {int(k): v for k, v in tasklist}

    # T/F if Nullpo is active or not
    try:
        return tasklist[currentPid] == 'javaw.exe'
    except KeyError:
        return False

    return {int(re.split(r' {3,}| Services| Console', i)[:2][::-1][0]):
            re.split(r' {3,}| Services| Console', i)[:2][::-1][1]
            for i in os.popen('tasklist').read().split('\n')[3:-1]
            }[win32process.GetWindowThreadProcessId(
                    win32gui.GetForegroundWindow())[1]] == 'javaw.exe'


def loopIsNullpo():
    ''' Loops until Nullpo is active, then loops until it's closed,
        then executes the methods to handle the new replays, then
        recurs backs to the loop

        Checks for it to be open/closed as often as is set up
        in config.ini

        Higher times will be less costly, but might miss
        games that are done in the first x seconds of
        Nullpo opening.  On my machine, (i5-5600K), each
        isNullpo() call takes up about .7% of the CPU
        for 2ish seconds, although results will vary
        across processors and machines.
    '''

    global CONFIG, TIMEZONE

    SLEEP_TIME = int(CONFIG['RUNTIME']['checkDelay'])

    # While the program's running, keep looping this
    while True:
        # Until nullpo is running
        while not isNullpo():
            print('looking for nullpo ' + str(datetime.datetime.now()))
            # Checks for nullpo as often as specified in CONFIG.ini
            time.sleep(SLEEP_TIME)

        else:  # When nullpo is active,
            print('Nullpo Started')

            # If a file was created after the startTime,
            # then it'll be tracked into the DB.
            startTime = datetime.datetime.now(tz=TIMEZONE)

            while isNullpo():
                time.sleep(SLEEP_TIME)
                print('Nullpo still open ' + str(datetime.datetime.now()))

            else:
                print('Nullpo Closed')
                # Runs through all the new files, and parses
                # and inserts them into the DB
                findReplays(startTime=startTime)


def parseReplay(name):
    ''' Runs through a .rep file (nullpo replays)
        and finds all the important data

        Uses hella regex to find all the important data

        If the mode is line race, then it uses a dictionary of the
        possible final goals to determine if the game finished.  This
        strategy is VERY imperfect, but I'm not aware of a better way.
        If the game didn't finish but you lost on a number of lines
        that could be finished on by a normal mode, it will false
        positive on it finishing and misassign the mode just because
        Nullpo doesn't record the goal in the replay file.

        Outputs a tuple with all the important stats
            Output Indexes:
                0: Dict of stats from the replay, keyed by stat name
                1: Name of mode
                2: If it's a line race, the goal #, otherwise just None
                3: ISO 8061 format of the time that the game either
                   ended or started, not sure how Nullpo tracks it
                4: Bool of whether or not the game was finished if
                   it's a line race, just exists to not log incomplete
                   data and f-ed up goals bc of how you have to find
                   the goal value
    '''

    global REPLAY_PATH

    finished = True

    # Saves the replay data into a variable as a list
    with open(REPLAY_PATH + name) as replay:
        replayData = replay.readlines()

    # Finds all the statistics in replayData, uses regex to
    # remove the 0.statistics and the \n's
    #        |---'0.statistics' or \n---|
    stats = [(re.sub(r'0\.statistics\.|\n', '', i)).split('=')
             for i in replayData if i.startswith('0.statistics.')]

    # Convert into a dict, split by the equals sign
    #        |-Name of stat-| |----Value of stat---|
    stats = {k: v for k, v in stats}

    # Finds the name of the mode, index gets group 2, which is the mode name
    #                |---Find the mode---| |Joins replayData list|
    mode = re.findall(r'(name\.mode=)(.*)', ' '.join(replayData))[0][1]

    if mode == 'LINE RACE':
        # The possible line numbers for each line race goal.
        # This is the easiest way to this that I could think of
        # Nescessary because the .rep files don't actually store
        # the goal directly for some reason (why Kitaru)
        GOAL_DICT = {10: 10, 11: 10, 12: 10, 13: 10,
                     20: 20, 21: 20, 22: 20, 23: 20,
                     40: 40, 41: 40, 42: 40, 43: 40,
                     100: 100, 101: 100, 102: 100, 103: 100}

        try:
            goal = GOAL_DICT[stats['lines']]
        except KeyError:
            goal = None
            finished = False
    else:
        goal = None

    # Yeah i know, it was yelling at me when
    # i formatted it more reasonably
    timeStamp = name.replace(
        '_', '-', 2).replace(
        '_', 'T', 1).replace(
        '_', '-', 2).replace(
        '.rep', '')

    return (stats, mode, goal, timeStamp, finished)


def findReplays(startTime=None):
    ''' Goes through the replays folder, and checks if there are any
        new replays, then inserts them into the DB

        Is HELLA inneficient bro, O(n^99999)

        Can also be run to log all non-tracked replays
        by leaving startTime as None

        startTime is the point for the modified time after which the
        method will start inserting the replay into the database.
    '''

    global CONFIG, DB, IGNORE_REPS, IGNORE_MODES, REPLAY_PATH

    filesInReplay = os.listdir(REPLAY_PATH)

    # Basically, if it's a first time setup and the 'Track Past Games'
    # flag is enabled in config.ini
    if not startTime:
        # Just for duplicate checking
        GAMES_TRACKED = [i + '.rep' for i in DB.execute(
            'SELECT fileName FROM GamesTracked').fetchall()]

        for rep in filesInReplay:
            if rep not in GAMES_TRACKED:
                insertIntoDB(parseReplay(rep), rep)

    else:
        for rep in filesInReplay:
            # If it was modified after Nullpo was started
            if modTime(rep, True) > startTime:
                print(f'Inserting {rep}, os.mtime = {modTime(rep, True)}' +
                      f', start time = {startTime}')
                insertIntoDB(parseReplay(rep), rep)

    DB.commit()


def insertIntoDB(replayData, repName, commit=False):
    ''' Inserts the files from findReplays() into the
        database.

        Also makes sure the game finished if it
        was a line race, and doesn't log it bc goals are not
        really possibly to check if a game didn't finish.

        Also, if it is a line race, it'll run a different
        SQL query to insert the goal as well, and if it's
        not a line race, it'll leave goal as the default NULL.

        Params:
        1. replayData is the output of parseReplays()
            Tuple Indexes:
                0: Dict of stats from the replay, keyed by stat name
                1: Name of mode
                2: If it's a line race, the goal #, otherwise just None
                3: ISO 8061 format of the time that the game either
                   ended or started, not sure how Nullpo tracks it
                4: Bool of whether or not the game was finished if
                   it's a line race, just exists to not log incomplete
                   data and f-ed up goals bc of how you have to find
                   the goal value

        2. repName is the name of the replay file that's being
           inserted into the DB, including '.rep'

        3. commit tells the function whether or not it should commit,
           if there is only one file being inserted.  Not used in the
           main body of NullpoTracker, but if this function is being
           used incidentally, like to insert a single file and not as
           part of findReplays(), it can just automatically commit the
           data to the DB.
    '''

    global DB

    print(f'DB inserting {replayData[1]}, PPS {replayData[0]["pps"]} and ' +
          f'time {replayData[0]["time"]}')

    # If it's a line race and if it finished,
    if replayData[1] == 'LINE RACE' and replayData[4]:
        DB.execute("INSERT INTO GamesTracked" +
                   "(fileName,time,PPS,mode,score,goal,timeStamp)" +
                   "VALUES ('{}', {}, {}, '{}', {}, {}, '{}');".format(
                       # Name of the file, time statistic, PPS
                       repName, replayData[0]['time'], replayData[0]['pps'],
                       #    Mode,           Score
                       replayData[1], replayData[0]['score'],
                       # Goal,    When the game happened
                       replayData[2], replayData[3]
                   ))
    # If it finished (Really only to avoid unfinished
    # line races being logged in this case, other modes
    # wouldn't have finished equal to False),
    elif replayData[4]:
        DB.execute("INSERT OR IGNORE INTO GamesTracked " +
                   "(fileName,time,PPS,mode,score,timeStamp) " +
                   "VALUES ('{}', {}, {}, '{}', {}, '{}');".format(
                       # Name of the file, time statistic, PPS
                       repName, replayData[0]['time'], replayData[0]['pps'],
                       #    Mode,             Score,     When the game happened
                       replayData[1], replayData[0]['score'], replayData[3]
                   ))
    # If the game wasn't finished (line race only),
    else:
        print('not finished')

    if commit:
        print('committed')
        DB.commit()


if __name__ == "__main__":
    checkAndHandleIgnores()
    loopIsNullpo()
