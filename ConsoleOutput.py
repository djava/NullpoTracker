import sqlite3
import datetime

DB = sqlite3.connect('./NullpoTracker.db')


def startOutput():

    command = input('Input: ')

    COMMAND_DICT = {
        'list': listAll
    }

    COMMAND_DICT[command]()


def listAll():
    global DB

    gamesInDB = DB.execute('SELECT ' +
                           'fileName, time, mode, PPS, timeStamp, goal ' +
                           'FROM GamesTracked;').fetchall()

    print('      FILE NAME             TIME            MODE' +
          '             PPS            DATE/TIME')
    print('-' * 91)
    for game in gamesInDB:
        if game[2] == 'LINE RACE':
            mode = f'LINE RACE ({game[5]})'
        else:
            mode = game[2]

        time = str(datetime.timedelta(seconds=game[1]))

        print(game[0] + ' ' * 4 + time + mode.center(26, ' ') +
              str(round(game[3], 4)) + ' ' * 6 +
              str(game[4][::-1].replace('-', ':', 2))[::-1])


listAll()

#       FILE NAME             TIME            MODE             PPS            DATE/TIME
# -------------------------------------------------------------------------------------------
# 2019_04_13_14_31_00.rep    0:14:50     LINE RACE (40)      2.0376      2019-04-13 14-40-44
