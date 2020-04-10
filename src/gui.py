from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QTableWidgetItem, QCheckBox,
                             QApplication, QTableWidget, QPushButton,
                             QMenu, QAction, QComboBox, QListWidgetItem,
                             QWidget)
from PyQt5.QtWidgets import QAbstractItemView as QAbsItemView
from PyQt5.QtGui import QStandardItem, QMouseEvent, QIcon
from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel, QDateTime
from ui_NullpoTracker import Ui_NullpoTracker
from enum import IntEnum, Enum, auto
import csv
from datetime import datetime, timedelta as tdelta
import time
import statistics
import math
from os import path
import ctypes

import globalVars
from gameTracker import dataCollection


CSV_FILE = open('internal/GameLog.csv', 'r')
CSV_READER = list(csv.DictReader(CSV_FILE))
ignoredReplaysFile = open('internal/ignoredReplays.txt', 'r+')
ignoredReplaysList = [i.strip() for i in ignoredReplaysFile.readlines()]


class gameTrackerIndexes(IntEnum):
    IGNORED = 0
    FILE_NAME = 1
    MODE = 2
    PPS = 3
    TIME = 4
    SCORE = 5
    PIECES = 6
    LINES = 7


class DateRangeComboBoxIndexes(IntEnum):
    TODAY = 0
    THIS_WEEK = 1
    THIS_MONTH = 2
    THIS_YEAR = 3
    ALL_TIME = 4
    CUSTOM = 5


class statisticsRadioButtons(Enum):
    AVERAGE = auto()
    MEDIAN = auto()
    MAD = auto()
    EXTREMA = auto()
    PERCENTILE = auto()


class NullpoTrackerGui(QMainWindow, Ui_NullpoTracker):
    framerate = int(globalVars.CONFIG['OTHER']['framerate'])
    hiddenFromMode = set()
    hiddenFromTime = set()

    def __init__(self):
        super(NullpoTrackerGui, self).__init__()
        self.setWindowIcon(QIcon('icon.ico'))

        self.setupUi(self)
        self.gameTracker.itemSelectionChanged.connect(self.gridClickHandler)
        self.gameTracker.cellDoubleClicked.connect(self.gridDoubleClickHandler)
        self.setGridColumnWidths()
        self.gameTracker.sortByColumn(
            gameTrackerIndexes.FILE_NAME, Qt.DescendingOrder)

        for row, i in zip(range(len(CSV_READER)), CSV_READER):
            self.addReplayToTracker(i, row)

        self.gameTracker.setSortingEnabled(True)
        self.ModeSelectorOpenButton.clicked.connect(
            self.modeSelectorButtonClickHandler)
        self.ModeSelectorOpenButton.setText('All Modes Enabled')
        self.ModeSelectorComboBox.setVisible(False)

        self.fillModeSelector()
        self.ModeSelectorComboBox.itemClicked.connect(
            self.modeSelectorClickHandler)
        self.setModeSelectorButtonText()

        self.DateRangeComboBox.addItems(
            ['Last 24 Hours', 'Last Week', 'Last Month',
             'Last Year', 'All Time', 'Custom'])
        self.DateRangeComboBox.setCurrentIndex(
            DateRangeComboBoxIndexes.ALL_TIME)
        self.DateRangeComboBox.currentIndexChanged.connect(
            self.dateRangeComboBoxChangedHandler)
        self.ToDateTimeSelector.setCalendarPopup(True)
        self.FromDateTimeSelector.setCalendarPopup(True)
        self.ToDateTimeSelector.setDateTime(datetime.now())
        self.FromDateTimeSelector.setDateTime(datetime.now() - tdelta(hours=1))

        self.ToDateTimeSelector.dateTimeChanged.connect(
            self.updateHiddenReplays)
        self.FromDateTimeSelector.dateTimeChanged.connect(
            self.updateHiddenReplays)

        self.ToDTNowButton.clicked.connect(
            self.toDTNowButtonPressedHandler)
        self.FromDTNowButton.clicked.connect(
            self.fromDTNowButtonPressedHandler)

        self.hideIgnoredCheckBox.clicked.connect(self.updateHiddenReplays)

        self.MeanRadioButton.clicked.connect(
            self.meanRadioButtonClickedHandler)
        self.MedianRadioButton.clicked.connect(
            self.medianRadioButtonClickedHandler)
        self.StdevRadioButton.clicked.connect(
            self.StdevRadioButtonClickedHandler)
        self.PercentileSpinBox.setEnabled(False)
        self.ExtremaRadioButton.clicked.connect(
            self.extremaRadioButtonClickedHandler)
        self.PercentileRadioButton.clicked.connect(
            self.percentileRadioButtonOrSpinBoxClickedHandler)
        self.PercentileSpinBox.valueChanged.connect(
            self.percentileRadioButtonOrSpinBoxClickedHandler)

        self.reloadStatistics()

        self.menuButtonRefresh.triggered.connect(
            self.refreshButtonClickedHandler)
        self.menuButtonExit.triggered.connect(exit)

    def closeModeSelectorSlot(self):
        self.ModeSelectorComboBox.setVisible(False)

    def setGridColumnWidths(self):
        self.gameTracker.setColumnWidth(gameTrackerIndexes.IGNORED, 15)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.FILE_NAME, 137)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.MODE, 125)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.PPS, 40)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.TIME, 58)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.SCORE, 58)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.PIECES, 48)
        self.gameTracker.setColumnWidth(gameTrackerIndexes.LINES, 37)

    def addReplayToTracker(self, rep: dict, row):
        self.gameTracker.insertRow(self.gameTracker.rowCount())
        GT = self.gameTracker
        RC = GT.rowCount()

        timeStr = str(
            tdelta(0, float(rep['time']) / self.framerate))
        if '.' not in timeStr:
            timeStr += '.000'
        timeStr = timeStr[:10]

        GTItemStrings = [
            '✓' if rep['fileName'] not in ignoredReplaysList else '✖',
            rep['fileName'],
            rep['mode'],
            str(round(float(rep['pps']), 3)).ljust(5, '0'),
            timeStr,
            rep['score'],
            rep['pieces'],
            rep['lines'],
        ]

        for col, i in zip(range(9), GTItemStrings):
            item = QTableWidgetItem()
            item.setText(i)
            item.setWhatsThis(str(row))
            if i == '✓' or i == '✖':
                item.setTextAlignment(Qt.AlignCenter)
            elif i.replace('.', '').isnumeric():
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            GT.setItem(RC - 1, col, item)

    def gridClickHandler(self):
        GTI = gameTrackerIndexes
        selectedRow = self.gameTracker.selectedItems()
        rowNumber = self.gameTracker.selectedIndexes()[0].row()
        CSV_SELECTION = list(CSV_READER)[rowNumber]
        self.SelectionNameStat.setText(selectedRow[GTI.FILE_NAME].text())
        self.SelectionModeStat.setText(selectedRow[GTI.MODE].text())

        self.SelectionPPSStat.setText(CSV_SELECTION['pps'])
        self.SelectionTimeStat.setText(
            str(tdelta(0, (float(CSV_SELECTION['time']) / self.framerate))
                ).rstrip('0').ljust(7, '0'))
        self.selectionScoreName.setText('Score:')
        self.selectionScoreStat.setText(selectedRow[GTI.SCORE].text())
        self.SelectionLinesStat.setText(selectedRow[GTI.LINES].text())
        self.SelectionPiecesStat.setText(selectedRow[GTI.PIECES].text())

    def gridDoubleClickHandler(self, row, col):
        if col == 0:
            selectedItem = self.gameTracker.item(row, col)
            if selectedItem.text() == '✓':
                selectedItem.setText('✖')
                writeToIgnoredReplays(self.gameTracker.item(row, 1).text())
            else:
                selectedItem.setText('✓')
                deleteReplayfromIgnored(self.gameTracker.item(row, 1).text())
        self.reloadStatistics()

    def fillModeSelector(self):
        item = QListWidgetItem('All')
        item.setCheckState(Qt.Checked)
        self.ModeSelectorComboBox.addItem(item)
        item = QListWidgetItem('None')
        item.setCheckState(Qt.Unchecked)
        self.ModeSelectorComboBox.addItem(item)

        modesList = sorted(list({i['mode'] for i in CSV_READER}))
        if 'LINE RACE (100)' in modesList and 'LINE RACE (40)' in modesList:
            del modesList[modesList.index('LINE RACE (100)')]
            modesList.insert(
                modesList.index('LINE RACE (40)') + 1, 'LINE RACE (100)')
        for i in modesList:
            item = QListWidgetItem()
            item.setText(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.ModeSelectorComboBox.addItem(item)

    def modeSelectorButtonClickHandler(self):
        self.ModeSelectorComboBox.setVisible(
            not self.ModeSelectorComboBox.isVisible())
        self.ModeSelectorComboBox.raise_()

    def modeSelectorClickHandler(self, item: QListWidgetItem):
        INDEX_ALL = 0
        INDEX_NONE = 1
        index = self.ModeSelectorComboBox.indexFromItem(item)
        if index.row() == INDEX_ALL:
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_ALL))\
                .setCheckState(Qt.Checked)
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_NONE))\
                .setCheckState(Qt.Unchecked)
            for i in range(2, self.ModeSelectorComboBox.count()):
                item = self.ModeSelectorComboBox.itemFromIndex(
                    index.siblingAtRow(i))
                item.setCheckState(Qt.Checked)
        elif index.row() == INDEX_NONE:
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_NONE))\
                .setCheckState(Qt.Checked)
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_ALL))\
                .setCheckState(Qt.Unchecked)
            for i in range(2, self.ModeSelectorComboBox.count()):
                item = self.ModeSelectorComboBox.itemFromIndex(
                    index.siblingAtRow(i))
                item.setCheckState(False)

        else:
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_NONE))\
                .setCheckState(Qt.Unchecked)
            self.ModeSelectorComboBox\
                .itemFromIndex(index.siblingAtRow(INDEX_ALL))\
                .setCheckState(Qt.Unchecked)
            if item.checkState():
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
        self.updateHiddenReplays()
        self.setModeSelectorButtonText()

    def updateHiddenReplays(self, uselessArg=None):
        global CSV_READER
        GT = self.gameTracker
        GTI = gameTrackerIndexes
        DR_INDEXES = DateRangeComboBoxIndexes
        DT_NOW = datetime.now()
        INTERVAL_DT_DICT = {
            DR_INDEXES.TODAY: tdelta(days=1),
            DR_INDEXES.THIS_WEEK: tdelta(weeks=1),
            DR_INDEXES.THIS_MONTH: tdelta(weeks=4),
            DR_INDEXES.THIS_YEAR: tdelta(weeks=52)
        }
        dateRangeIndex = self.DateRangeComboBox.currentIndex()
        enabledModes = []
        for i in range(2, self.ModeSelectorComboBox.count()):
            index = self.ModeSelectorComboBox.model().index(i, 0)
            item = self.ModeSelectorComboBox.itemFromIndex(index)
            if item.checkState():
                enabledModes.append(item.text())

        if dateRangeIndex <= DR_INDEXES.THIS_YEAR:
            for row in range(GT.rowCount()):
                ignrItem = GT.itemFromIndex(GT.model().index(row, GTI.IGNORED))
                modeItem = GT.itemFromIndex(GT.model().index(row, GTI.MODE))
                csvRow = CSV_READER[int(modeItem.whatsThis())]
                timeSinceGame = DT_NOW - datetime.fromisoformat(
                    csvRow['timeStamp'])
                if self.hideIgnoredCheckBox.isChecked():
                    if timeSinceGame < INTERVAL_DT_DICT[dateRangeIndex] and \
                       modeItem.text() in enabledModes and \
                       ignrItem.text() == '✓':
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
                else:
                    if timeSinceGame < INTERVAL_DT_DICT[dateRangeIndex] and \
                       modeItem.text() in enabledModes:
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
        elif dateRangeIndex == DR_INDEXES.ALL_TIME:
            if self.hideIgnoredCheckBox.isChecked():
                for row in range(GT.rowCount()):
                    item = GT.itemFromIndex(GT.model().index(row, GTI.MODE))
                    ignr = GT.itemFromIndex(GT.model().index(row, GTI.IGNORED))
                    if item.text() in enabledModes and ignr.text() == '✓':
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
            else:
                for row in range(GT.rowCount()):
                    item = GT.itemFromIndex(GT.model().index(row, GTI.MODE))
                    if item.text() in enabledModes:
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
        elif dateRangeIndex == DR_INDEXES.CUSTOM:
            fromDT = self.FromDateTimeSelector.dateTime().toPyDateTime()
            toDT = self.ToDateTimeSelector.dateTime().toPyDateTime()
            if self.hideIgnoredCheckBox.isChecked():
                for row in range(GT.rowCount()):
                    ignr = GT.itemFromIndex(GT.model().index(row, GTI.IGNORED))
                    mode = GT.itemFromIndex(GT.model().index(row, GTI.MODE))
                    csvRow = CSV_READER[int(modeItem.whatsThis())]
                    timeOfRep = datetime.fromisoformat(csvRow['timeStamp'])
                    if timeOfRep > fromDT and timeOfRep < toDT \
                       and mode.text() in enabledModes \
                       and ignr.text() == '✓':
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
            else:
                for row in range(GT.rowCount()):
                    mode = GT.itemFromIndex(GT.model().index(row, GTI.MODE))
                    csvRow = CSV_READER[int(mode.whatsThis())]
                    timeOfRep = datetime.fromisoformat(csvRow['timeStamp'])
                    if timeOfRep > fromDT and timeOfRep < toDT \
                       and mode.text() in enabledModes:
                        GT.showRow(row)
                    else:
                        GT.hideRow(row)
        self.reloadStatistics()

    def setModeSelectorButtonText(self):
        BUTTON = self.ModeSelectorOpenButton
        MODE_SELECTOR = self.ModeSelectorComboBox
        totalModes = MODE_SELECTOR.count() - 2
        enabledModes = 0
        for i in range(2, MODE_SELECTOR.count()):
            index = MODE_SELECTOR.model().index(i, 0)
            if MODE_SELECTOR.itemFromIndex(index).checkState() == Qt.Checked:
                enabledModes += 1

        if totalModes == enabledModes:
            BUTTON.setText('All Modes Enabled')
        else:
            BUTTON.setText(f'{enabledModes} Modes Enabled' +
                           f'({totalModes - enabledModes} Disabled)')

    def dateRangeComboBoxChangedHandler(self, index: int):
        if index == DateRangeComboBoxIndexes.CUSTOM:
            self.CustomDateRangeSelector.setEnabled(True)
        else:
            self.CustomDateRangeSelector.setEnabled(False)
        self.updateHiddenReplays()

    def toDTNowButtonPressedHandler(self):
        self.ToDateTimeSelector.setDateTime(datetime.now())

    def fromDTNowButtonPressedHandler(self):
        self.FromDateTimeSelector.setDateTime(datetime.now())

    def meanRadioButtonClickedHandler(self):
        self.AvgPPSName.setText('Avg PPS:')
        self.AvgTimeName.setText('Avg Time:')
        self.AvgScoreName.setText('Avg Score:')
        self.AvgLinesName.setText('Avg Lines:')
        self.AvgPiecesName.setText('Avg Pieces:')
        self.reloadStatistics()

    def medianRadioButtonClickedHandler(self):
        self.AvgPPSName.setText('Med PPS:')
        self.AvgTimeName.setText('Med Time:')
        self.AvgScoreName.setText('Med Score:')
        self.AvgLinesName.setText('Med Lines:')
        self.AvgPiecesName.setText('Med Pieces:')
        self.reloadStatistics()

    def StdevRadioButtonClickedHandler(self):
        self.AvgPPSName.setText('Dev. PPS:')
        self.AvgTimeName.setText('Dev. Time:')
        self.AvgScoreName.setText('Dev. Score:')
        self.AvgLinesName.setText('Dev. Lines:')
        self.AvgPiecesName.setText('Dev. Pieces:')
        self.reloadStatistics()

    def extremaRadioButtonClickedHandler(self):
        self.PercentileSpinBox.setEnabled(False)
        self.HighestPPSName.setText('Highest PPS:')
        self.LowestPPSName.setText('Lowest PPS:')
        self.HighestTimeName.setText('Highest Time:')
        self.LowestTimeName.setText('Lowest Time:')
        self.HighestPiecesName.setText('Highest Pieces:')
        self.LowestPiecesName.setText('Lowest Pieces:')
        self.HighestLinesName.setText('Highest Lines:')
        self.LowestLinesName.setText('Lowest Lines:')
        self.reloadStatistics()

    def percentileRadioButtonOrSpinBoxClickedHandler(self):
        self.PercentileSpinBox.setEnabled(True)
        perc = self.PercentileSpinBox.value()
        self.HighestPPSName.setText(f'{perc}% PPS:')
        self.LowestPPSName.setText(f'{100 - perc}% PPS:')
        self.HighestTimeName.setText(f'{perc}% Time:')
        self.LowestTimeName.setText(f'{100 - perc}% Time:')
        self.HighestPiecesName.setText(f'{perc}% Pieces:')
        self.LowestPiecesName.setText(f'{100 - perc}% Pieces:')
        self.HighestLinesName.setText(f'{perc}% Lines:')
        self.LowestLinesName.setText(f'{100 - perc}% Lines:')
        self.reloadStatistics()

    def reloadStatistics(self):
        global CSV_READER
        GT = self.gameTracker
        GTI = gameTrackerIndexes

        statsToTrack = ['pps', 'time', 'score', 'pieces', 'lines']
        statsDict = {}
        for col in statsToTrack:
            stat = []
            for row in range(GT.rowCount()):
                ignoredIndex = GT.model().index(row, GTI.IGNORED)
                csvRow = int(GT.itemFromIndex(ignoredIndex).whatsThis())
                if not GT.isRowHidden(row) \
                   and GT.itemFromIndex(ignoredIndex).text() == '✓':
                    stat.append(float(CSV_READER[csvRow][col]))
            statsDict[col] = sorted(stat)

        if not statsDict['pps']:
            self.AvgPPSStat.setText('')
            self.AvgTimeStat.setText('')
            self.AvgScoreStat.setText('')
            self.AvgLinesStat.setText('')
            self.AvgPiecesStat.setText('')
            self.HighestPPSStat.setText('')
            self.LowestPPSStat.setText('')
            self.HighestTimeStat.setText('')
            self.LowestTimeStat.setText('')
            self.HighestPiecesStat.setText('')
            self.LowestPiecesStat.setText('')
            self.HighestLinesStat.setText('')
            self.LowestLinesStat.setText('')
            return

        if self.MeanRadioButton.isChecked():
            stat = statistics.mean(statsDict['pps'])
            self.AvgPPSStat.setText(str(round(stat, 5)))
            stat = statistics.mean(statsDict['time'])
            stat = str(tdelta(0, (float(stat) / self.framerate)))[:11]
            self.AvgTimeStat.setText(stat)
            stat = statistics.mean(statsDict['score'])
            self.AvgScoreStat.setText(str(round(stat, 2)))
            stat = statistics.mean(statsDict['pieces'])
            self.AvgPiecesStat.setText(str(round(stat, 2)))
            stat = statistics.mean(statsDict['lines'])
            self.AvgLinesStat.setText(str(round(stat, 3)))
        elif self.MedianRadioButton.isChecked():
            stat = statistics.median(statsDict['pps'])
            self.AvgPPSStat.setText(str(round(stat, 5)))
            stat = statistics.median(statsDict['time'])
            stat = str(tdelta(0, (float(stat) / self.framerate)))[:11]
            self.AvgTimeStat.setText(stat)
            stat = statistics.median(statsDict['score'])
            self.AvgScoreStat.setText(str(int(stat)))
            stat = statistics.median(statsDict['pieces'])
            self.AvgPiecesStat.setText(str(int(stat)))
            stat = statistics.median(statsDict['lines'])
            self.AvgLinesStat.setText(str(int(stat)))
        elif self.StdevRadioButton.isChecked():
            stat = statistics.stdev(statsDict['pps'])
            self.AvgPPSStat.setText(str(round(stat, 4)))
            stat = statistics.stdev(statsDict['time'])
            self.AvgTimeStat.setText(str(round(stat, 4)))
            stat = statistics.stdev(statsDict['score'])
            self.AvgScoreStat.setText(str(round(stat, 4)))
            stat = statistics.stdev(statsDict['pieces'])
            self.AvgPiecesStat.setText(str(round(stat, 4)))
            stat = statistics.stdev(statsDict['lines'])
            self.AvgLinesStat.setText(str(round(stat, 4)))

        if self.ExtremaRadioButton.isChecked():
            self.HighestPPSStat.setText(str(max(statsDict['pps'])))
            self.LowestPPSStat.setText(str(min(statsDict['pps'])))
            timeStr = str(tdelta(0,
                                 float(max(statsDict['time'])) / self.framerate
                                 ))[:11]
            self.HighestTimeStat.setText(timeStr)
            timeStr = str(tdelta(0,
                                 float(min(statsDict['time'])) / self.framerate
                                 ))[:11]
            self.LowestTimeStat.setText(timeStr)
            self.HighestPiecesStat.setText(str(max(statsDict['pieces'])))
            self.LowestPiecesStat.setText(str(min(statsDict['pieces'])))
            self.HighestLinesStat.setText(str(max(statsDict['lines'])))
            self.LowestLinesStat.setText(str(min(statsDict['lines'])))
        elif self.PercentileRadioButton.isChecked():
            percentile = self.PercentileSpinBox.value()
            self.HighestPPSStat.setText(
                str(findPercentile(statsDict['pps'], percentile)))
            self.LowestPPSStat.setText(
                str(findPercentile(statsDict['pps'], 100 - percentile)))
            self.HighestTimeStat.setText(
                str(findPercentile(statsDict['time'], percentile)))
            self.LowestTimeStat.setText(
                str(findPercentile(statsDict['time'], 100 - percentile)))
            self.HighestPiecesStat.setText(
                str(findPercentile(statsDict['pieces'], percentile)))
            self.LowestPiecesStat.setText(
                str(findPercentile(statsDict['pieces'], 100 - percentile)))
            self.HighestLinesStat.setText(
                str(findPercentile(statsDict['lines'], percentile)))
            self.LowestLinesStat.setText(
                str(findPercentile(statsDict['lines'], 100 - percentile)))

    def refreshButtonClickedHandler(self):
        global CSV_READER, CSV_FILE
        GT = self.gameTracker
        dataCollection.findReplays()
        CSV_FILE.seek(0)
        CSV_READER = list(csv.DictReader(CSV_FILE))
        for i in range(GT.rowCount()-1, -1, -1):
            GT.removeRow(i)

        for row, i in zip(range(len(CSV_READER)), CSV_READER):
            self.addReplayToTracker(i, row)

        self.hiddenFromMode = set()
        self.hiddenFromTime = set()
        self.dateRangeComboBoxChangedHandler(
            self.DateRangeComboBox.currentIndex())
        for i in range(2, self.ModeSelectorComboBox.count()):
            isChecked = self.ModeSelectorComboBox.item(i).checkState()
            self.ModeSelectorComboBox.item(i).setCheckState(
                Qt.Unchecked if isChecked else Qt.Checked)
            self.modeSelectorClickHandler(self.ModeSelectorComboBox.item(i))

        GT.sortByColumn(
            gameTrackerIndexes.FILE_NAME, Qt.DescendingOrder)
        self.reloadStatistics()


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


def findPercentile(arr: list, perc: float):
    indexOfPerc = (len(arr)-1) * (perc/100)
    if indexOfPerc.is_integer():
        return arr[int(indexOfPerc)]
    else:
        ret = statistics.mean(
            [arr[math.floor(indexOfPerc)], arr[math.ceil(indexOfPerc)]])
        if ret.is_integer():
            return int(ret)
        else:
            return ret


def initGui():
    app = QApplication([])
    app.setWindowIcon(QIcon('icon.ico'))
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('.')
    window = NullpoTrackerGui()
    window.show()
    app.exec()
    ignoredReplaysFile.close()
    CSV_FILE.close()


if __name__ == '__main__':
    # dataCollection.findReplays()
    CSV_FILE.seek(0)
    CSV_READER = list(csv.DictReader(CSV_FILE))
    initGui()
