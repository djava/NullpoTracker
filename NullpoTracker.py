# TODO (order of short-termedness):
# 1. Add a console output system
# 2. Check for new files better (Current is very inefficient)
# 3. Add an electron good-looking output app


from win32 import win32gui
from win32 import win32process
import os
import re
import time
import datetime
import sqlite3
import configparser
import pickle
from timezones import CURRENT_TIMEZONE as TIMEZONE
from timezones import UTC


DB = sqlite3.connect('NullpoTracker.db')

CONFIG = configparser.ConfigParser()
CONFIG.read('CONFIG.ini')

REPLAY_PATH = CONFIG['SETUP']['nullpoPath'] + '/replay/'

with open('./ignoreReps.txt') as iR:
    IGNORE_REPS = iR.read().split('\n')
with open('./ignoreModes.txt') as iM:
    IGNORE_MODES = iM.read().split('\n')

OPEN_TIME = datetime.datetime.now(tz=TIMEZONE)
with open('lastTimeOpenedDT.pickle', 'rb+') as lTO:
    try:
        LAST_TIME_OPENED = pickle.load(lTO)
    except EOFError:
        LAST_TIME_OPENED = datetime.datetime(1970, 1, 1)
with open('lastTimeOpenedDT.pickle', 'rb+') as lTO:
    pickle.dump(OPEN_TIME, lTO, pickle.HIGHEST_PROTOCOL)


def modTime(path, *includeReplayPath):
    global REPLAY_PATH, UTC
    if includeReplayPath:
        return datetime.datetime(1970, 1, 1, tzinfo=UTC) + datetime.timedelta(
            seconds=(os.path.getmtime(REPLAY_PATH + path)))

    else:
        return datetime.datetime(1970, 1, 1, tzinfo=UTC) + datetime.timedelta(
            seconds=(os.path.getmtime(path)))


def checkAndHandleIgnores():
    global LAST_TIME_OPENED, IGNORE_MODES, IGNORE_REPS, DB
    time.sleep(2)

    modIgnoreReps = modTime('./ignoreReps.txt') > LAST_TIME_OPENED

    if modIgnoreReps:
        for rep in IGNORE_REPS:
            DB.execute(f"UPDATE GamesTracked\
                        SET time=NULL,\
                            PPS=NULL,\
                            mode=NULL,\
                            score=NULL,\
                            ignore=1\
                        WHERE fileName='{rep}'';")

    if IGNORE_MODES != ['']:
        for mode in IGNORE_MODES:
            DB.execute(f"UPDATE GamesTracked\
                        SET time=NULL,\
                            PPS=NULL,\
                            mode=NULL,\
                            score=NULL,\
                            ignore=1\
                        WHERE mode='{mode}';")

    DB.commit()


def isNullpo(Active=True):
    '''
    Returns true if the current active window is Nullpo, false if it's not

    Only works on Windows

    Gets the PID for the current active window as currentPid
    Compares that against a dictionary of parsed tasklist data
    If currentPid is the same as the pid for javaw.exe (Nullpo), return True

    Will produce a false positive if you use other applications
    that run as javaw.exe, IDK how to fix that
    '''
#                |------Converts a HWND to a PID------|
    currentPid = win32process.GetWindowThreadProcessId(
        # |-Gets HWND of active window-|
        win32gui.GetForegroundWindow())[1]

    tasklist = []
    # Gets the output of running tasklist, and splits it by line,
    # first 3 lines are garbage, last line is blank
    for i in os.popen('tasklist').read().split('\n')[3:-1]:

        # Splits each line in tasklist into just the
        # name and PID, adds it to a list
        tasklist.append(re.split(r' {3,}| Services| Console', i)[:2])

    # Converts the name and PID into a dict to find Nullpo more easily
    tasklist = {i[0]: int(i[1]) for i in tasklist}

    # If nullpo is open,
    if 'javaw.exe' in tasklist.keys():

        if Active and tasklist['javaw.exe'] == currentPid:
            # If nullpo is the current window, return true
            # (sub-listed to prevent IndexErrors)
            return True
        elif not Active:
            return True

    # Return false if either one is false
    return False


def loopIsNullpo():
    '''
    Loops until Nullpo is active
    '''

    global CONFIG, TIMEZONE

    # Until nullpo is running
    while not isNullpo():
        print('looking for nullpo')
        # Checks for nullpo as often as specified in CONFIG.ini
        time.sleep(int(CONFIG['RUNTIME']['checkDelay']))

    else:  # When nullpo is active,
        print('Nullpo Started')

        startTime = datetime.datetime.now(tz=TIMEZONE)

        while isNullpo(Active=False):
            time.sleep(int(CONFIG['RUNTIME']['checkDelay']))
        else:
            print('Nullpo Closed')
            findReplays(startTime=startTime)
            loopIsNullpo()


def parseReplay(name):
    '''
    Runs through a .rep file (nullpo replays)
    and finds all the important data
    '''

    global REPLAY_PATH

    # Saves the replay data into a variable as a list
    with open(REPLAY_PATH + name) as replay:
        replayData = replay.readlines()

    # Finds all the statistics in replayData, uses regex to
    # remove the 0.statistics and the \n's
    #       |-----0.statistics or \n-----|
    stats = [re.sub(r'0\.statistics\.|\n', '', i)
             for i in replayData if i.startswith('0.statistics.')]

    # Convert into a dict, split by the equals sign
    #        |-Name of stat-| |----Value of stat---|
    stats = {i.split('=')[0]: float(i.split('=')[1])
             for i in stats}

    # Finds the name of the mode, index gets group 2, which is the mode name
    #                |---Find the mode---| |Joins replayData list|
    mode = re.findall(r'(name\.mode=)(.*)', ' '.join(replayData))[0][1]

    if mode == 'LINE RACE':
        GOAL_DICT = {10: 10, 11: 10, 12: 10, 13: 10,
                     20: 20, 21: 20, 22: 20, 23: 20,
                     40: 40, 41: 40, 42: 40, 43: 40,
                     100: 100, 101: 100, 102: 100, 103: 100}

        goal = GOAL_DICT[stats['lines']]
    else:
        goal = None

    timeStamp = (f'{name[:4]}-{name[5:7]}-{name[8:10]} ' +
                 f'{name[11:13]}-{name[14:16]}-{name[17:19]}')

    return (stats, mode, goal, timeStamp)


def findReplays(startTime=None):

    global CONFIG, DB, IGNORE_REPS, IGNORE_MODES, REPLAY_PATH

    filesInReplay = os.listdir(REPLAY_PATH)

    newReplays = []
    if not startTime:
        GAMES_TRACKED = [i + '.rep' for i in DB.execute(
            'SELECT fileName FROM GamesTracked').fetchall()]
        for rep in filesInReplay:
            if rep not in GAMES_TRACKED:
                replayData = parseReplay(rep)
                insertIntoDB(replayData, rep)
    else:
        for rep in filesInReplay:
            if modTime(rep, True) > startTime:
                print(f'Inserting {rep}, os.mtime = {modTime(rep, True)}\
, start time = {startTime}')
                insertIntoDB(parseReplay(rep), rep)

    DB.commit()


def insertIntoDB(replayData, repName, commit=False):
    global DB

    print(f'DB inserting {replayData[1]}, PPS {replayData[0]["pps"]} and ' +
          f'time {replayData[0]["time"]}')

    if replayData[2]:
        DB.execute("INSERT INTO GamesTracked" +
                   "(fileName,time,PPS,mode,score,goal,timeStamp)" +
                   "VALUES ('{}', {}, {}, '{}', {}, {}, '{}');".format(
                       repName, replayData[0]['time'], replayData[0]['pps'],
                       replayData[1], replayData[0]['score'],
                       replayData[2], replayData[3]
                   ))
    else:
        DB.execute("INSERT OR IGNORE INTO GamesTracked " +
                   "(fileName,time,PPS,mode,score,timeStamp) " +
                   "VALUES ('{}', {}, {}, '{}', {}, '{}');".format(
                       repName, replayData[0]['time'], replayData[0]['pps'],
                       replayData[1], replayData[0]['score'], replayData[3]
                   ))

    if commit:
        print('committed')
        DB.commit()

checkAndHandleIgnores()
loopIsNullpo()
