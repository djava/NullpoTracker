import sqlite3
import datetime
from matplotlib import pyplot as plt

DB = sqlite3.connect('./NullpoTracker.db')


def startOutput():

    command = input('Command: ')

    COMMAND_DICT = {
        'list': listAll,
        'avg': getAvgs,
        'graph': makeGraphs
    }

    COMMAND_DICT[command]()


def listAll():
    global DB

    gamesInDB = DB.execute('SELECT ' +
                           'fileName, time, mode, PPS, timeStamp, goal ' +
                           'FROM GamesTracked;').fetchall()

    print(' ' * 6 + 'FILE NAME' + ' ' * 13 + 'TIME' + ' ' * 12 + 'MODE' +
          ' ' * 13 + 'PPS' + ' ' * 12 + 'DATE/TIME')
    print('-' * 91)
    for game in gamesInDB:
        if game[2] == 'LINE RACE':
            mode = f'LINE RACE ({game[5]})'
        else:
            mode = game[2]

        time = str(datetime.timedelta(seconds=game[1]))

        print(game[0] + ' ' * 4 + time + mode.center(26, ' ') +
              str(round(game[3], 4)).ljust(6, '0') + ' ' * 6 +
              str(game[4][::-1].replace('-', ':', 2))[::-1])


def getAvgs():
    avg = input('Which statistic? ')
    mode = input('Which mode? ')
    if mode.upper() == 'LINE RACE':
        goal = input('What goal? ')
    else:
        goal = 'all'

    STAT_DICT = {
        'time': 'time',
        'pps': 'PPS',
        'score': 'score',
    }

    print('\n')
    # try:
    if avg == 'exit' or mode == 'exit':
        return
    elif mode == 'LINE RACE' and goal != 'all':
        if goal == 'exit':
            return

        else:
            output = (DB.execute(f'SELECT AVG({STAT_DICT[avg.lower()]}) ' +
                                 f'FROM GamesTracked ' +
                                 f'WHERE mode="LINE RACE" AND goal={goal};')
                        .fetchone()[0])

    elif mode != 'all':
        output = (DB.execute(f'SELECT AVG({STAT_DICT[avg]}) ' +
                             f'FROM GamesTracked ' +
                             f'WHERE mode="{mode.upper()}";')
                    .fetchone()[0])

    else:
        output = (DB.execute(f'SELECT AVG({STAT_DICT[avg.lower()]}) ' +
                             f'FROM GamesTracked;')
                    .fetchone()[0])

    if avg == 'pps':
        print(round(output, 6))
    elif avg == 'time':
        time = datetime.timedelta(seconds=output / 60)
        print(f'{time}'[2:])
        # output = f'{}:{}.{}'
    # except:
        # print('Invalid Input')
        # getAvgs()


def makeGraphs():

    global DB

    stat = input('Which statistic? ')
    mode = input('Which mode? ')
    if mode.lower() == 'line race':
        goal = int(input('Which goal? '))
    else:
        goal = None
    days = int(input('how far back? (days) '))
    STAT_DICT = {
        'time': 'time',
        'pps': 'PPS',
        'score': 'score',
    }
    runLR = True if mode.lower() == 'line race' and goal != 'all' else False

    afterTime = datetime.date.today() - datetime.timedelta(days=days)
    if runLR:
        timeData = DB.execute(f'SELECT timeStamp FROM GamesTracked ' +
                              f'WHERE timeStamp >= Datetime(' +
                              f'"{afterTime} 00:00:00") AND ' +
                              f'goal = {goal};'
                              ).fetchall()

        statData = DB.execute(f'SELECT {STAT_DICT[stat]} FROM GamesTracked' +
                              f'WHERE timeStamp >= Datetime(' +
                              f'"{afterTime} 00:00:00") ' +
                              f'AND goal = {goal};'
                              ).fetchall()

    else:
        timeData = DB.execute('SELECT timeStamp FROM GamesTracked ' +
                              'WHERE timeStamp >= Datetime(' +
                              f'"{afterTime} 00:00:00");'
                              ).fetchall()

        statData = DB.execute(f'SELECT {STAT_DICT[stat]} FROM GamesTracked' +
                              f'WHERE timeStamp >= Datetime(' +
                              f'"{afterTime} 00:00:00");'
                              ).fetchall()

    timeData = [datetime.datetime.fromisoformat(i[0][::-1]
                                                .replace('-', ':', 2)
                                                .replace(' ', 'T')[::-1])
                for i in timeData]

    plt.plot(timeData, statData)
    plt.show()


makeGraphs()
# startOutput()
