from PyQt5.QtWidgets import (QMainWindow, QTableWidgetItem, QCheckBox,
                             QApplication, QTableWidget, QPushButton,)
from PyQt5.QtWidgets import QAbstractItemView as QAbsItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QModelIndex
from ui_NullpoTracker import Ui_NullpoTracker
from enum import IntEnum
import csv
from datetime import timedelta as tdelta
from os import path


class gameTrackerIndexes(IntEnum):
    IGNORED = 0
    FILE_NAME = 1
    MODE = 2
    PPS = 3
    TIME = 4
    SCORE = 5
    PIECES = 6
    LINES = 7
    GOAL = 8


class NullpoTrackerGui(QMainWindow, Ui_NullpoTracker):
    def __init__(self):
        super(NullpoTrackerGui, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.gameTracker.itemSelectionChanged.connect(self.gridClickHandler)
        self.gameTracker.cellDoubleClicked.connect(self.gridDoubleClickHandler)
        self.setGridColumnWidths()

        for i in list(CSV_READER):
            self.addReplayToTracker(i)

        self.gameTracker.setSortingEnabled(True)

    def setGridColumnWidths(self):
        self.gameTracker.setColumnWidth(gameTrackerIndexes.IGNORED, 15)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.FILE_NAME, 137)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.MODE, 90)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.PPS, 40)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.TIME, 58)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.SCORE, 52)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.PIECES, 43)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.LINES, 37)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.GOAL, 35)

    def addReplayToTracker(self, rep: dict):
        self.gameTracker.insertRow(self.gameTracker.rowCount())
        GT = self.gameTracker
        RC = GT.rowCount()

        GTItemStrings = [
            '✓' if rep['fileName'] not in ignoredReplaysList else '✖',
            rep['fileName'],
            rep['mode'],
            str(round(float(rep['pps']), 3)).ljust(5, '0'),
            str(tdelta(0, float(rep['time'])/60))[:-4],
            rep['score'],
            rep['pieces'],
            rep['lines'],
            rep['goal'],
        ]

        for col, i in zip(range(9), GTItemStrings):
            item = QTableWidgetItem()
            item.setText(i)
            if i == '✓' or i == '✖':
                item.setTextAlignment(Qt.AlignCenter)
            elif i.replace('.', '').isnumeric():
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            GT.setItem(RC - 1, col, item)

    def gridClickHandler(self):
        GTI = gameTrackerIndexes
        selectedRow = self.gameTracker.selectedItems()
        rowNumber = self.gameTracker.indexFromItem(selectedRow[0]).row()
        CSV_SELECTION = list(CSV_READER)[rowNumber]
        self.SelectionNameStat.setText(selectedRow[GTI.FILE_NAME].text())
        if selectedRow[GTI.MODE].text() == 'MARATHON':
            goal = selectedRow[GTI.GOAL].text()
            self.SelectionModeStat.setText(
                f'MARATHON ({goal if goal != "None" else "Endless"})')
        else:
            self.SelectionModeStat.setText(selectedRow[GTI.MODE].text())

        self.SelectionPPSStat.setText(CSV_SELECTION['pps'])
        self.SelectionTimeStat.setText(
            str(tdelta(0, (float(CSV_SELECTION['time']) / 60))).rstrip('0'))

        if selectedRow[GTI.MODE].text() == 'LINE RACE':
            self.SelectionScoreGoalName.setText('Goal:')
            self.SelectionScoreGoalStat.setText(selectedRow[GTI.GOAL].text())
        else:
            self.SelectionScoreGoalName.setText('Score:')
            self.SelectionScoreGoalStat.setText(selectedRow[GTI.SCORE].text())

        self.SelectionLinesStat.setText(selectedRow[GTI.LINES].text())
        self.SelectionPiecesStat.setText(selectedRow[GTI.PIECES].text())

    def gridDoubleClickHandler(self, row, col):
        if col == 0:
            csvFieldNames = [
                'fileName', 'mode', 'time', 'pps', 'score', 'lines',
                'pieces', 'finished', 'goal', 'timeStamp', 'ignored'
            ]
            selectedItem = self.gameTracker.item(row, col)
            if selectedItem.text() == '✓':
                selectedItem.setText('✖')
                writeToIgnoredReplays(self.gameTracker.item(row, 1).text())
            else:
                selectedItem.setText('✓')
                deleteReplayfromIgnored(self.gameTracker.item(row, 1).text())


def writeToIgnoredReplays(string: str, newLine=True):
    global ignoredReplaysFile, ignoredReplaysList
    ignoredReplaysFile.seek(0, 2)
    if newLine:
        ignoredReplaysFile.write(string + '\n')
    else:
        ignoredReplaysFile.write(string)
    ignoredReplaysFile.seek(0)
    ignoredReplaysList = ignoredReplaysFile.readlines()


def deleteReplayfromIgnored(name: str):
    global ignoredReplaysFile, ignoredReplaysList
    ignoredReplaysFile.seek(0)
    ignoredList = ignoredReplaysFile.readlines()
    ignoredReplaysFile.seek(0)
    ignoredReplaysFile.truncate()
    for i in ignoredList:
        if i.strip() != name:
            ignoredReplaysFile.write(i)
    ignoredReplaysFile.seek(0)
    ignoredReplaysList = ignoredReplaysFile.readlines()


CSV_FILE = open('internal/GameLog.csv', 'r')
CSV_READER = list(csv.DictReader(CSV_FILE))
ignoredReplaysFile = open('internal/ignoredReplays.txt', 'r+')
ignoredReplaysList = [i.strip() for i in ignoredReplaysFile.readlines()]
app = QApplication([])
window = NullpoTrackerGui()
window.show()
app.exec()
ignoredReplaysFile.close()
CSV_FILE.close()
