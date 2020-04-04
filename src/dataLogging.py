import globalVars
import csv


def insertReplayIntoCSV(rep):
    with open('internal/gameLog.csv', 'a') as gameLogFile:
        lineToInsert = [
            rep.fileName,
            rep.mode,
            rep.stats['time'],
            rep.stats['pps'],
            rep.stats['score'],
            rep.stats['lines'],
            rep.stats['totalPieceLocked'],
            rep.finished,
            rep.lineRaceGoal,
            rep.timeStamp,
            'FALSE'
        ]
        gameLogFile.write(','.join([str(i) for i in lineToInsert]) + '\n')
