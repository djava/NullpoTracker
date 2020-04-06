import re
import os
import csv

import globalVars
import utils
from . import dataLogging


class replayData(object):
    def __init__(self, name):
        self.fileName = name

        with open(globalVars.REPLAY_PATH + name) as replay:
            replayLines = replay.readlines()

        self.stats = {}
        for i in replayLines:
            if i.startswith('0.statistics.'):
                stat = i.replace('0.statistics.', '')[:-1].split('=')
                self.stats[stat[0]] = stat[1]

        for i in replayLines:
            if i.startswith('name.mode='):
                self.mode = i.replace('name.mode=', '')[:-1]
                break

        if self.mode == 'LINE RACE':
            self.isLineRace = True
            lineRaceGoalDict = {'0': 20, '1': 40, '2': 100, '3': 10}
            for i in replayLines:
                if i.startswith('linerace.goaltype.-1='):
                    self.goal = lineRaceGoalDict[i[-2]]
                    break
            self.finished = int(self.stats['lines']) > self.goal

        elif self.mode == 'MARATHON':
            self.isLineRace = False
            marathonGoalDict = {'0': 150, '1': 200, '2': 'None'}
            for i in replayLines:
                if i.startswith('marathon.gametype='):
                    self.goal = marathonGoalDict[i[-2]]
                    break
            if i[-2] != '2':
                self.finished = int(self.stats['lines']) > self.goal
            else:
                self.finished = None
        else:
            self.isLineRace = False
            self.goal = None
            self.finished = None

        # Converts YYYY_MM_DD_HH_MM_SS.rep into YYYY-MM-DDTHH-MM-SS (ISO 8601)
        self.timeStamp = name.replace('_', '-', 2) \
                             .replace('_', 'T', 1) \
                             .replace('_', '-', 2) \
                             .replace('.rep', '')


def findReplays(startTime=None):
    ''' Goes through the replays folder, and checks if there are any
        new replays, then inserts them into the CSV

        Can also be run to log all non-tracked replays
        by leaving startTime as None

        startTime is the point for the modified time after which the
        method will start inserting the replay into the database.
        Using startTime should have the same effect as not using it
        after the initial setup, it'll just be slower.
    '''

    # if utils.modTime(globalVars.REPLAY_PATH) < globalVars.LAST_TIME_OPENED:
    #     return

    filesInReplay = os.listdir(globalVars.REPLAY_PATH)
    replaysLogged = 0
    if not startTime:
        try:
            gamesTracked = [i['fileName'] for i in
                            csv.DictReader(open('internal/GameLog.csv', 'r'))]
        except KeyError:
            gamesTracked = []

        for rep in filesInReplay:
            if rep not in gamesTracked:
                dataLogging.insertReplayIntoCSV(replayData(rep))
                replaysLogged += 1

    else:
        for rep in filesInReplay:
            if utils.modTime(rep, True) > startTime:
                dataLogging.insertReplayIntoCSV(replayData(rep))
                replaysLogged += 1
