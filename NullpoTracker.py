import os
import re
import time
from win32 import win32gui
from win32 import win32process
import datetime
import json
import sqlite3

database = sqlite3.connect('./NullpoTracker.db')


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
    '''
    Loops until Nullpo is active
    '''

    wasActive = False
    active = isNullpo()

    # Until nullpo is running
    while not active:

        time.sleep(3)
        active = isNullpo()

        # This will evantually be replaced with something better
        print('not active')

    else:  # When nullpo is active
        # This will evantually be replaced with something better
        print('Nullpo is active')

        wasActive = True


def parseReplay(path):
    '''
    Runs through a .rep file (nullpo replays)
    and finds all the important data
    '''

    # Saves the replay data into a variable as a list
    with open(path) as replay:
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

    timestamp = [re.findall(r'(timestamp.time=)(.*)',
                            ' '.join(replayData))[0][1].split(r'\:'),
                 re.findall(r'(timestamp.date=)(.*)',
                            ' '.join(replayData))[0][1].split(r'/')
                 ]
    timestamp = datetime.datetime(
        timestamp[1][0], timestamp[1][1], timestamp[1][2],
        hour=timestamp[0][0], minute=timestamp[0][1]
    )

    return (stats, mode, timestamp)
