import os
import re
import time
from win32 import win32gui
from win32 import win32process
import datetime
import json
import sqlite3


def isNullpo():
    '''
    Returns true if the current active window is Nullpo, false if it's not

    Only works on Windows

    Gets the PID for the current active window as currentPid
    Compares that against a dictionary of parsed tasklist data
    If currentPid is the same as the pid for javaw.exe (Nullpo), return True

    Will produce a false positive if you use other
    applications that run as javaw.exe
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

        # If nullpo is the current window, return true
        # (sub-listed to prevent IndexErrors)
        if tasklist['javaw.exe'] == currentPid:
            return True

    # Return false if either one is false
    return False


def loopIsNullpo():
    ''''''
    Active = isNullpo()
    while not Active:
        time.sleep(3)
        Active = isNullpo()
        print('not active')
    else:
        print('Nullpo is active')


database = sqlite3.connect('./NullpoTracker.db')


def parseReplay(path):
    with open(path) as replay:
        replayData = replay.readlines()

    replayStats = [i for i in replayData if i.startswith('0.statistics.')]

    for i in range(len(replayStats)):
        replayStats[i] = re.sub(r'0\.statistics\.|\n', r'', replayStats[i])

    replayStats = {i.split('=')[0]: float(i.split('=')[1])
                   for i in replayStats}

    mode = re.findall(r'(name\.mode=)(.*)', ' '.join(replayData))[0][1]

    timestamp = [re.findall(r'(timestamp.time=)(.*)',
                            ' '.join(replayData))[0][1].split(r'\:'),
                 re.findall(r'(timestamp.date=)(.*)',
                            ' '.join(replayData))[0][1].split(r'/')
                 ]
    timestamp = datetime.datetime(
        timestamp[1][0], timestamp[1][1], timestamp[1][2],
        hour=timestamp[0][0], minute=timestamp[0][1]
                      )
