import globalVars
import csv


def insertReplayIntoCSV(rep):
    with open('internal/gameLog.csv', 'a') as gameLogFile:
        if rep.mode in ['LINE RACE', 'MARATHON']:
            lineToInsert = [
                    rep.fileName,
                    rep.mode + f' ({rep.goal})',
                    rep.stats['time'],
                    rep.stats['pps'],
                    rep.stats['score'],
                    rep.stats['lines'],
                    rep.stats['totalPieceLocked'],
                    rep.timeStamp
                ]
            gameLogFile.write(','.join([str(i) for i in lineToInsert]) + '\n')
        else:
            lineToInsert = [
                rep.fileName,
                rep.mode,
                rep.stats['time'],
                rep.stats['pps'],
                rep.stats['score'],
                rep.stats['lines'],
                rep.stats['totalPieceLocked'],
                rep.timeStamp
            ]
            gameLogFile.write(','.join([str(i) for i in lineToInsert]) + '\n')
