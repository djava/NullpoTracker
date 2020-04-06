from PyQt5 import QtGui
from PyQt5.QtWidgets import (QMainWindow, QTableWidgetItem, QCheckBox,
                             QApplication, QTableWidget, QPushButton,
                             QMenu, QAction, QComboBox, QListWidgetItem)
from PyQt5.QtWidgets import QAbstractItemView as QAbsItemView
from PyQt5.QtGui import QStandardItem, QMouseEvent
from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel, pyqtSignal
from checkableComboBox import CheckableComboBox
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
        self.ModeSelectorOpenButton.clicked.connect(
            self.modeSelectorButtonClickHandler)
        self.ModeSelectorOpenButton.setText('All Modes Enabled')
        self.ModeSelectorComboBox.setVisible(False)

        item = QListWidgetItem('All')
        item.setCheckState(Qt.Checked)
        self.ModeSelectorComboBox.addItem(item)
        item = QListWidgetItem('None')
        item.setCheckState(Qt.Unchecked)
        self.ModeSelectorComboBox.addItem(item)
        for i in sorted(list({i['mode'] for i in CSV_READER})):
            item = QListWidgetItem()
            item.setText(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
            self.ModeSelectorComboBox.addItem(item)
        self.ModeSelectorComboBox.itemClicked.connect(
            self.modeSelectorClickHandler)
        self.setModeSelectorButtonText()

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

        timeStr = str(tdelta(0, float(rep['time'])/60))
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
            str(tdelta(0, (float(CSV_SELECTION['time']) / 60))).rstrip('0')
                                                               .ljust(7, '0'))

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
                self.showModeOnGrid(item.text())
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
                self.hideModeFromGrid(item.text())

        else:
            if item.checkState():
                item.setCheckState(Qt.Unchecked)
                self.hideModeFromGrid(item.text())
            else:
                item.setCheckState(Qt.Checked)
                self.showModeOnGrid(item.text())
        self.setModeSelectorButtonText()

    def hideModeFromGrid(self, mode: str):
        GT = self.gameTracker
        MODE_INDEX = gameTrackerIndexes.MODE
        toBeRemoved = []
        rowZeroIndex = GT.model().index(0, gameTrackerIndexes.MODE)
        for i in range(GT.rowCount()):
            if GT.itemFromIndex(rowZeroIndex.siblingAtRow(i)).text() == mode:
                GT.hideRow(i)

    def showModeOnGrid(self, mode: str):
        GT = self.gameTracker
        MODE_INDEX = gameTrackerIndexes.MODE
        toBeRemoved = []
        rowZeroIndex = GT.model().index(0, gameTrackerIndexes.MODE)
        for i in range(GT.rowCount()):
            if GT.itemFromIndex(rowZeroIndex.siblingAtRow(i)).text() == mode:
                if GT.isRowHidden(i):
                    GT.showRow(i)

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
