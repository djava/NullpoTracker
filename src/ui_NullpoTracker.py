# -*- coding: utf-8 -*-

# Form implementation generated from reading file 'NullpoTrackerQtDesigner.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from enum import IntEnum


class Ui_NullpoTracker(object):
    def setupUi(self, NullpoTracker):
        NullpoTracker.setObjectName("NullpoTracker")
        NullpoTracker.resize(798, 633)
        self.Window = QtWidgets.QWidget(NullpoTracker)
        self.Window.setObjectName("Window")
        self.StatisticsFrame = QtWidgets.QFrame(self.Window)
        self.StatisticsFrame.setGeometry(QtCore.QRect(570, 70, 221, 331))
        self.StatisticsFrame.setMouseTracking(False)
        self.StatisticsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StatisticsFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.StatisticsFrame.setObjectName("StatisticsFrame")
        self.StatisticsLabel = QtWidgets.QLabel(self.StatisticsFrame)
        self.StatisticsLabel.setGeometry(QtCore.QRect(10, 0, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.StatisticsLabel.setFont(font)
        self.StatisticsLabel.setTextFormat(QtCore.Qt.AutoText)
        self.StatisticsLabel.setObjectName("StatisticsLabel")
        self.WhichAvgSelector = QtWidgets.QWidget(self.StatisticsFrame)
        self.WhichAvgSelector.setGeometry(QtCore.QRect(10, 30, 201, 21))
        self.WhichAvgSelector.setObjectName("WhichAvgSelector")
        self.MeanRadioButton = QtWidgets.QRadioButton(self.WhichAvgSelector)
        self.MeanRadioButton.setGeometry(QtCore.QRect(0, 0, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MeanRadioButton.setFont(font)
        self.MeanRadioButton.setChecked(True)
        self.MeanRadioButton.setAutoExclusive(True)
        self.MeanRadioButton.setObjectName("MeanRadioButton")
        self.MedianRadioButton = QtWidgets.QRadioButton(self.WhichAvgSelector)
        self.MedianRadioButton.setGeometry(QtCore.QRect(70, 0, 71, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.MedianRadioButton.setFont(font)
        self.MedianRadioButton.setObjectName("MedianRadioButton")
        self.MADRadioButton = QtWidgets.QRadioButton(self.WhichAvgSelector)
        self.MADRadioButton.setGeometry(QtCore.QRect(140, 0, 51, 17))
        self.MADRadioButton.setObjectName("MADRadioButton")
        self.Statistics = QtWidgets.QWidget(self.StatisticsFrame)
        self.Statistics.setGeometry(QtCore.QRect(10, 50, 201, 281))
        self.Statistics.setObjectName("Statistics")
        self.AvgStats = QtWidgets.QWidget(self.Statistics)
        self.AvgStats.setGeometry(QtCore.QRect(0, 0, 201, 101))
        self.AvgStats.setObjectName("AvgStats")
        self.AvgTime = QtWidgets.QWidget(self.AvgStats)
        self.AvgTime.setGeometry(QtCore.QRect(0, 20, 201, 21))
        self.AvgTime.setObjectName("AvgTime")
        self.AvgTimeName = QtWidgets.QLabel(self.AvgTime)
        self.AvgTimeName.setGeometry(QtCore.QRect(0, 0, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgTimeName.setFont(font)
        self.AvgTimeName.setObjectName("AvgTimeName")
        self.AvgTimeStat = QtWidgets.QLabel(self.AvgTime)
        self.AvgTimeStat.setGeometry(QtCore.QRect(100, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgTimeStat.setFont(font)
        self.AvgTimeStat.setObjectName("AvgTimeStat")
        self.AvgLines = QtWidgets.QWidget(self.AvgStats)
        self.AvgLines.setGeometry(QtCore.QRect(0, 60, 201, 21))
        self.AvgLines.setObjectName("AvgLines")
        self.AvgLinesName = QtWidgets.QLabel(self.AvgLines)
        self.AvgLinesName.setGeometry(QtCore.QRect(0, 0, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgLinesName.setFont(font)
        self.AvgLinesName.setObjectName("AvgLinesName")
        self.AvgLinesStat = QtWidgets.QLabel(self.AvgLines)
        self.AvgLinesStat.setGeometry(QtCore.QRect(100, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgLinesStat.setFont(font)
        self.AvgLinesStat.setObjectName("AvgLinesStat")
        self.AvgPieces = QtWidgets.QWidget(self.AvgStats)
        self.AvgPieces.setGeometry(QtCore.QRect(0, 80, 201, 21))
        self.AvgPieces.setObjectName("AvgPieces")
        self.AvgPiecesName = QtWidgets.QLabel(self.AvgPieces)
        self.AvgPiecesName.setGeometry(QtCore.QRect(0, 0, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgPiecesName.setFont(font)
        self.AvgPiecesName.setObjectName("AvgPiecesName")
        self.AvgPiecesStat = QtWidgets.QLabel(self.AvgPieces)
        self.AvgPiecesStat.setGeometry(QtCore.QRect(100, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgPiecesStat.setFont(font)
        self.AvgPiecesStat.setObjectName("AvgPIecesStat")
        self.AvgPPS = QtWidgets.QWidget(self.AvgStats)
        self.AvgPPS.setGeometry(QtCore.QRect(0, 0, 201, 21))
        self.AvgPPS.setObjectName("AvgPPS")
        self.AvgPPSName = QtWidgets.QLabel(self.AvgPPS)
        self.AvgPPSName.setGeometry(QtCore.QRect(0, 0, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgPPSName.setFont(font)
        self.AvgPPSName.setObjectName("AvgPPSName")
        self.AvgPPSStat = QtWidgets.QLabel(self.AvgPPS)
        self.AvgPPSStat.setGeometry(QtCore.QRect(100, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgPPSStat.setFont(font)
        self.AvgPPSStat.setObjectName("AvgPPSStat")
        self.AvgScore = QtWidgets.QWidget(self.AvgStats)
        self.AvgScore.setGeometry(QtCore.QRect(0, 40, 201, 21))
        self.AvgScore.setObjectName("AvgScore")
        self.AvgScoreName = QtWidgets.QLabel(self.AvgScore)
        self.AvgScoreName.setGeometry(QtCore.QRect(0, 0, 80, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgScoreName.setFont(font)
        self.AvgScoreName.setObjectName("AvgScoreName")
        self.AvgScoreStat = QtWidgets.QLabel(self.AvgScore)
        self.AvgScoreStat.setGeometry(QtCore.QRect(100, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.AvgScoreStat.setFont(font)
        self.AvgScoreStat.setObjectName("AvgScoreStat")
        self.ExtremeStats = QtWidgets.QWidget(self.Statistics)
        self.ExtremeStats.setGeometry(QtCore.QRect(0, 120, 201, 161))
        self.ExtremeStats.setObjectName("ExtremeStats")
        self.LinesExtrema = QtWidgets.QWidget(self.ExtremeStats)
        self.LinesExtrema.setGeometry(QtCore.QRect(0, 120, 201, 41))
        self.LinesExtrema.setObjectName("LinesExtrema")
        self.HighestLines = QtWidgets.QWidget(self.LinesExtrema)
        self.HighestLines.setGeometry(QtCore.QRect(0, 0, 201, 21))
        self.HighestLines.setObjectName("HighestLines")
        self.HighestLinesName = QtWidgets.QLabel(self.HighestLines)
        self.HighestLinesName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestLinesName.setFont(font)
        self.HighestLinesName.setObjectName("HighestLinesName")
        self.HighestLinesStat = QtWidgets.QLabel(self.HighestLines)
        self.HighestLinesStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestLinesStat.setFont(font)
        self.HighestLinesStat.setObjectName("HighestLinesStat")
        self.LowestLines = QtWidgets.QWidget(self.LinesExtrema)
        self.LowestLines.setGeometry(QtCore.QRect(0, 20, 201, 21))
        self.LowestLines.setObjectName("LowestLines")
        self.LowestLinesName = QtWidgets.QLabel(self.LowestLines)
        self.LowestLinesName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestLinesName.setFont(font)
        self.LowestLinesName.setObjectName("LowestLinesName")
        self.LowestLinesStat = QtWidgets.QLabel(self.LowestLines)
        self.LowestLinesStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestLinesStat.setFont(font)
        self.LowestLinesStat.setObjectName("LowestLinesStat")
        self.PiecesExtrema = QtWidgets.QWidget(self.ExtremeStats)
        self.PiecesExtrema.setGeometry(QtCore.QRect(0, 80, 201, 41))
        self.PiecesExtrema.setObjectName("PiecesExtrema")
        self.HighestPieces = QtWidgets.QWidget(self.PiecesExtrema)
        self.HighestPieces.setGeometry(QtCore.QRect(0, 0, 201, 21))
        self.HighestPieces.setObjectName("HighestPieces")
        self.HighestPiecesName = QtWidgets.QLabel(self.HighestPieces)
        self.HighestPiecesName.setGeometry(QtCore.QRect(0, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestPiecesName.setFont(font)
        self.HighestPiecesName.setObjectName("HighestPiecesName")
        self.HighestPiecesStat = QtWidgets.QLabel(self.HighestPieces)
        self.HighestPiecesStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestPiecesStat.setFont(font)
        self.HighestPiecesStat.setObjectName("HighestPiecesStat")
        self.LowestPieces = QtWidgets.QWidget(self.PiecesExtrema)
        self.LowestPieces.setGeometry(QtCore.QRect(0, 20, 201, 21))
        self.LowestPieces.setObjectName("LowestPieces")
        self.LowestPiecesName = QtWidgets.QLabel(self.LowestPieces)
        self.LowestPiecesName.setGeometry(QtCore.QRect(0, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestPiecesName.setFont(font)
        self.LowestPiecesName.setObjectName("LowestPiecesName")
        self.LowestPiecesStat = QtWidgets.QLabel(self.LowestPieces)
        self.LowestPiecesStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestPiecesStat.setFont(font)
        self.LowestPiecesStat.setObjectName("LowestPiecesStat")
        self.PPSExtrema = QtWidgets.QWidget(self.ExtremeStats)
        self.PPSExtrema.setGeometry(QtCore.QRect(0, 0, 201, 41))
        self.PPSExtrema.setObjectName("PPSExtrema")
        self.HighestPPS = QtWidgets.QWidget(self.PPSExtrema)
        self.HighestPPS.setGeometry(QtCore.QRect(0, 0, 201, 21))
        self.HighestPPS.setObjectName("HighestPPS")
        self.HighestPPSName = QtWidgets.QLabel(self.HighestPPS)
        self.HighestPPSName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestPPSName.setFont(font)
        self.HighestPPSName.setObjectName("HighestPPSName")
        self.HighestPPSStat = QtWidgets.QLabel(self.HighestPPS)
        self.HighestPPSStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestPPSStat.setFont(font)
        self.HighestPPSStat.setObjectName("HighestPPSStat")
        self.LowestPPS = QtWidgets.QWidget(self.PPSExtrema)
        self.LowestPPS.setGeometry(QtCore.QRect(0, 20, 201, 21))
        self.LowestPPS.setObjectName("LowestPPS")
        self.LowestPPSName = QtWidgets.QLabel(self.LowestPPS)
        self.LowestPPSName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestPPSName.setFont(font)
        self.LowestPPSName.setObjectName("LowestPPSName")
        self.LowestPPSStat = QtWidgets.QLabel(self.LowestPPS)
        self.LowestPPSStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestPPSStat.setFont(font)
        self.LowestPPSStat.setObjectName("LowestPPSStat")
        self.TimeExtrema = QtWidgets.QWidget(self.ExtremeStats)
        self.TimeExtrema.setGeometry(QtCore.QRect(0, 40, 201, 41))
        self.TimeExtrema.setObjectName("TimeExtrema")
        self.HighestTime = QtWidgets.QWidget(self.TimeExtrema)
        self.HighestTime.setGeometry(QtCore.QRect(0, 0, 201, 21))
        self.HighestTime.setObjectName("HighestTime")
        self.HighestTimeName = QtWidgets.QLabel(self.HighestTime)
        self.HighestTimeName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestTimeName.setFont(font)
        self.HighestTimeName.setObjectName("HighestTimeName")
        self.HighestTimeStat = QtWidgets.QLabel(self.HighestTime)
        self.HighestTimeStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.HighestTimeStat.setFont(font)
        self.HighestTimeStat.setObjectName("HighestTimeStat")
        self.LowestTime = QtWidgets.QWidget(self.TimeExtrema)
        self.LowestTime.setGeometry(QtCore.QRect(0, 20, 201, 21))
        self.LowestTime.setObjectName("LowestTime")
        self.LowestTimeName = QtWidgets.QLabel(self.LowestTime)
        self.LowestTimeName.setGeometry(QtCore.QRect(0, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestTimeName.setFont(font)
        self.LowestTimeName.setObjectName("LowestTimeName")
        self.LowestTimeStat = QtWidgets.QLabel(self.LowestTime)
        self.LowestTimeStat.setGeometry(QtCore.QRect(100, 0, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.LowestTimeStat.setFont(font)
        self.LowestTimeStat.setObjectName("LowestTimeStat")
        self.WhichExtremaSelector = QtWidgets.QWidget(self.StatisticsFrame)
        self.WhichExtremaSelector.setGeometry(QtCore.QRect(10, 150, 201, 21))
        self.WhichExtremaSelector.setObjectName("WhichExtremaSelector")
        self.ExtremaRadioButton = QtWidgets.QRadioButton(
            self.WhichExtremaSelector)
        self.ExtremaRadioButton.setGeometry(QtCore.QRect(0, 2, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ExtremaRadioButton.setFont(font)
        self.ExtremaRadioButton.setChecked(True)
        self.ExtremaRadioButton.setAutoExclusive(True)
        self.ExtremaRadioButton.setObjectName("ExtremaRadioButton")
        self.PercentileRadioButton = QtWidgets.QRadioButton(
            self.WhichExtremaSelector)
        self.PercentileRadioButton.setGeometry(QtCore.QRect(74, 2, 81, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PercentileRadioButton.setFont(font)
        self.PercentileRadioButton.setObjectName("PercentileRadioButton")
        self.PercentileSpinBox = QtWidgets.QSpinBox(self.WhichExtremaSelector)
        self.PercentileSpinBox.setGeometry(QtCore.QRect(152, 2, 51, 17))
        self.PercentileSpinBox.setMaximum(100)
        self.PercentileSpinBox.setProperty("value", 100)
        self.PercentileSpinBox.setObjectName("PercentileSpinBox")
        self.PercentileSpinBox.setSuffix('%')
        self.Settings = QtWidgets.QWidget(self.Window)
        self.Settings.setGeometry(QtCore.QRect(10, 10, 791, 51))
        self.Settings.setObjectName("Settings")
        self.ModesEnabled = QtWidgets.QWidget(self.Settings)
        self.ModesEnabled.setGeometry(QtCore.QRect(10, 0, 221, 51))
        self.ModesEnabled.setObjectName("ModesEnabled")
        self.ModesEnabledLabel = QtWidgets.QLabel(self.ModesEnabled)
        self.ModesEnabledLabel.setGeometry(QtCore.QRect(0, 0, 151, 16))
        self.ModesEnabledLabel.setObjectName("ModesEnabledLabel")
        self.ModeSelectorOpenButton = QtWidgets.QPushButton(self.ModesEnabled)
        self.ModeSelectorOpenButton.setGeometry(QtCore.QRect(0, 20, 221, 21))
        self.ModeSelectorOpenButton.setObjectName("ModeSelectorOpenButton")
        self.ModeSelectorComboBox = QtWidgets.QListWidget(self.Window)
        self.ModeSelectorComboBox.setGeometry(QtCore.QRect(21, 50, 219, 140))
        self.ModeSelectorComboBox.setObjectName("ModeSelectorComboBox")
        self.ModeSelectorComboBox.raise_()
        self.DateRangeSelector = QtWidgets.QWidget(self.Settings)
        self.DateRangeSelector.setGeometry(QtCore.QRect(240, 0, 531, 51))
        self.DateRangeSelector.setObjectName("DateRangeSelector")
        self.DateRangeLabel = QtWidgets.QLabel(self.DateRangeSelector)
        self.DateRangeLabel.setGeometry(QtCore.QRect(10, 0, 71, 16))
        self.DateRangeLabel.setObjectName("DateRangeLabel")
        self.DateRangeComboBox = QtWidgets.QComboBox(self.DateRangeSelector)
        self.DateRangeComboBox.setGeometry(QtCore.QRect(10, 20, 191, 21))
        self.DateRangeComboBox.setObjectName("DateRangeComboBox")
        self.CustomDateRangeSelector = QtWidgets.QWidget(
                                                        self.DateRangeSelector)
        self.CustomDateRangeSelector.setGeometry(QtCore.QRect(230, 0, 291, 51))
        self.CustomDateRangeSelector.setObjectName("CustomDateRangeSelector")
        self.CustomDateRangeSelector.setEnabled(False)
        self.FromSelector = QtWidgets.QWidget(self.CustomDateRangeSelector)
        self.FromSelector.setGeometry(QtCore.QRect(0, 0, 141, 51))
        self.FromSelector.setObjectName("FromSelector")
        self.FromLabel = QtWidgets.QLabel(self.FromSelector)
        self.FromLabel.setGeometry(QtCore.QRect(0, 0, 47, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.FromLabel.setFont(font)
        self.FromLabel.setObjectName("FromLabel")
        self.FromDateTimeSelector = QtWidgets.QDateTimeEdit(self.FromSelector)
        self.FromDateTimeSelector.setGeometry(QtCore.QRect(0, 20, 131, 22))
        self.FromDateTimeSelector.setObjectName("FromDateTimeSelector")
        self.ToSelector = QtWidgets.QWidget(self.CustomDateRangeSelector)
        self.ToSelector.setGeometry(QtCore.QRect(160, 0, 141, 51))
        self.ToSelector.setObjectName("ToSelector")
        self.ToLabel = QtWidgets.QLabel(self.ToSelector)
        self.ToLabel.setGeometry(QtCore.QRect(0, 0, 47, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ToLabel.setFont(font)
        self.ToLabel.setObjectName("ToLabel")
        self.ToDateTimeSelector = QtWidgets.QDateTimeEdit(self.ToSelector)
        self.ToDateTimeSelector.setGeometry(QtCore.QRect(0, 20, 131, 22))
        self.ToDateTimeSelector.setObjectName("ToDateTimeSelector")
        self.gameTracker = QtWidgets.QTableWidget(self.Window)
        self.gameTracker.setGeometry(QtCore.QRect(10, 70, 551, 521))
        self.gameTracker.setColumnCount(9)
        self.gameTracker.setObjectName("gameTracker")
        self.gameTracker.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.gameTracker.setHorizontalHeaderItem(8, item)

        self.gameTracker.horizontalHeader().setCascadingSectionResizes(True)
        self.gameTracker.horizontalHeader().setDefaultSectionSize(59)
        self.gameTracker.horizontalHeader().setHighlightSections(True)
        self.gameTracker.horizontalHeader().setMinimumSectionSize(10)
        self.gameTracker.horizontalHeader().setSortIndicatorShown(True)
        self.gameTracker.horizontalHeader().setStretchLastSection(True)
        self.gameTracker.verticalHeader().setCascadingSectionResizes(False)
        self.gameTracker.verticalHeader().setDefaultSectionSize(15)
        self.gameTracker.verticalHeader().setVisible(False)

        self.gameTracker.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.gameTracker.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.gameTracker.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)

        self.SelectionFrame = QtWidgets.QFrame(self.Window)
        self.SelectionFrame.setGeometry(QtCore.QRect(570, 410, 221, 181))
        self.SelectionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SelectionFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.SelectionFrame.setObjectName("SelectionFrame")
        self.SelectionLabel = QtWidgets.QLabel(self.SelectionFrame)
        self.SelectionLabel.setGeometry(QtCore.QRect(0, 0, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SelectionLabel.setFont(font)
        self.SelectionLabel.setTextFormat(QtCore.Qt.AutoText)
        self.SelectionLabel.setObjectName("SelectionLabel")
        self.SelectionPPS = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionPPS.setGeometry(QtCore.QRect(10, 70, 200, 21))
        self.SelectionPPS.setObjectName("SelectionPPS")
        self.SelectionPPSName = QtWidgets.QLabel(self.SelectionPPS)
        self.SelectionPPSName.setGeometry(QtCore.QRect(0, 0, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionPPSName.setFont(font)
        self.SelectionPPSName.setObjectName("SelectionPPSName")
        self.SelectionPPSStat = QtWidgets.QLabel(self.SelectionPPS)
        self.SelectionPPSStat.setGeometry(QtCore.QRect(50, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionPPSStat.setFont(font)
        self.SelectionPPSStat.setObjectName("SelectionPPSStat")
        self.SelectionTime = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionTime.setGeometry(QtCore.QRect(10, 90, 200, 21))
        self.SelectionTime.setObjectName("SelectionTime")
        self.SelectionTimeName = QtWidgets.QLabel(self.SelectionTime)
        self.SelectionTimeName.setGeometry(QtCore.QRect(0, 0, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionTimeName.setFont(font)
        self.SelectionTimeName.setObjectName("SelectionTimeName")
        self.SelectionTimeStat = QtWidgets.QLabel(self.SelectionTime)
        self.SelectionTimeStat.setGeometry(QtCore.QRect(50, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionTimeStat.setFont(font)
        self.SelectionTimeStat.setObjectName("SelectionTimeStat")
        self.SelectionScoreGoal = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionScoreGoal.setGeometry(QtCore.QRect(10, 110, 200, 21))
        self.SelectionScoreGoal.setObjectName("SelectionScoreGoal")
        self.SelectionScoreGoalName = QtWidgets.QLabel(self.SelectionScoreGoal)
        self.SelectionScoreGoalName.setGeometry(QtCore.QRect(0, 0, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionScoreGoalName.setFont(font)
        self.SelectionScoreGoalName.setObjectName("SelectionScoreGoalName")
        self.SelectionScoreGoalStat = QtWidgets.QLabel(self.SelectionScoreGoal)
        self.SelectionScoreGoalStat.setGeometry(QtCore.QRect(50, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionScoreGoalStat.setFont(font)
        self.SelectionScoreGoalStat.setObjectName("SelectionScoreGoalStat")
        self.SelectionLines = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionLines.setGeometry(QtCore.QRect(10, 130, 200, 21))
        self.SelectionLines.setObjectName("SelectionLines")
        self.SelectionLinesName = QtWidgets.QLabel(self.SelectionLines)
        self.SelectionLinesName.setGeometry(QtCore.QRect(0, 0, 41, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionLinesName.setFont(font)
        self.SelectionLinesName.setObjectName("SelectionLinesName")
        self.SelectionLinesStat = QtWidgets.QLabel(self.SelectionLines)
        self.SelectionLinesStat.setGeometry(QtCore.QRect(50, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionLinesStat.setFont(font)
        self.SelectionLinesStat.setObjectName("SelectionLinesStat")
        self.SelectionPieces = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionPieces.setGeometry(QtCore.QRect(10, 150, 200, 21))
        self.SelectionPieces.setObjectName("SelectionPieces")
        self.SelectionPiecesName = QtWidgets.QLabel(self.SelectionPieces)
        self.SelectionPiecesName.setGeometry(QtCore.QRect(0, 0, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionPiecesName.setFont(font)
        self.SelectionPiecesName.setObjectName("SelectionPiecesName")
        self.SelectionPiecesStat = QtWidgets.QLabel(self.SelectionPieces)
        self.SelectionPiecesStat.setGeometry(QtCore.QRect(50, 0, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionPiecesStat.setFont(font)
        self.SelectionPiecesStat.setObjectName("SelectionPiecesStat")
        self.SelectionName = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionName.setGeometry(QtCore.QRect(10, 30, 201, 21))
        self.SelectionName.setObjectName("SelectionName")
        self.SelectionNameName = QtWidgets.QLabel(self.SelectionName)
        self.SelectionNameName.setGeometry(QtCore.QRect(0, 0, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionNameName.setFont(font)
        self.SelectionNameName.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.SelectionNameName.setObjectName("SelectionNameName")
        self.SelectionNameStat = QtWidgets.QLabel(self.SelectionName)
        self.SelectionNameStat.setGeometry(QtCore.QRect(46, 0, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.SelectionNameStat.setFont(font)
        self.SelectionNameStat.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
            | QtCore.Qt.AlignVCenter)
        self.SelectionNameStat.setObjectName("SelectionNameStat")
        self.SelectionMode = QtWidgets.QWidget(self.SelectionFrame)
        self.SelectionMode.setGeometry(QtCore.QRect(10, 50, 201, 21))
        self.SelectionMode.setObjectName("SelectionMode")
        self.SelectionModeName = QtWidgets.QLabel(self.SelectionMode)
        self.SelectionModeName.setGeometry(QtCore.QRect(0, 0, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionModeName.setFont(font)
        self.SelectionModeName.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.SelectionModeName.setObjectName("SelectionModeName")
        self.SelectionModeStat = QtWidgets.QLabel(self.SelectionMode)
        self.SelectionModeStat.setGeometry(QtCore.QRect(46, 0, 161, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SelectionModeStat.setFont(font)
        self.SelectionModeStat.setAlignment(
            QtCore.Qt.AlignLeading |
            QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.SelectionModeStat.setObjectName("SelectionModeStat")
        NullpoTracker.setCentralWidget(self.Window)
        self.MenuBar = QtWidgets.QMenuBar(NullpoTracker)
        self.MenuBar.setGeometry(QtCore.QRect(0, 0, 798, 21))
        self.MenuBar.setObjectName("MenuBar")
        self.menuMenu = QtWidgets.QMenu(self.MenuBar)
        self.menuMenu.setObjectName("menuMenu")
        NullpoTracker.setMenuBar(self.MenuBar)
        self.statusbar = QtWidgets.QStatusBar(NullpoTracker)
        self.statusbar.setObjectName("statusbar")
        NullpoTracker.setStatusBar(self.statusbar)
        self.menuButtonRefresh = QtWidgets.QAction(NullpoTracker)
        self.menuButtonRefresh.setObjectName("menuButtonRefresh")
        self.menuButtonExit = QtWidgets.QAction(NullpoTracker)
        self.menuButtonExit.setObjectName("menuButtonExit")
        self.menuMenu.addAction(self.menuButtonRefresh)
        self.menuMenu.addAction(self.menuButtonExit)
        self.MenuBar.addAction(self.menuMenu.menuAction())
        self.ModesEnabledLabel.setBuddy(self.ModeSelectorComboBox)
        self.DateRangeLabel.setBuddy(self.DateRangeComboBox)
        self.FromLabel.setBuddy(self.FromDateTimeSelector)
        self.ToLabel.setBuddy(self.ToDateTimeSelector)

        self.retranslateUi(NullpoTracker)
        QtCore.QMetaObject.connectSlotsByName(NullpoTracker)

    def retranslateUi(self, NullpoTracker):
        _translate = QtCore.QCoreApplication.translate
        NullpoTracker.setWindowTitle(_translate("NullpoTracker", "MainWindow"))
        self.StatisticsLabel.setText(_translate("NullpoTracker", "Statistics"))
        self.MeanRadioButton.setText(_translate("NullpoTracker", "Mean"))
        self.MedianRadioButton.setText(_translate("NullpoTracker", "Median"))
        self.MADRadioButton.setText(_translate("NullpoTracker", "MAD"))
        self.AvgTimeName.setText(_translate("NullpoTracker", "Avg Time:"))
        self.AvgTimeStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.AvgLinesName.setText(_translate("NullpoTracker", "Avg Lines:"))
        self.AvgLinesStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.AvgPiecesName.setText(_translate("NullpoTracker", "Avg Pieces:"))
        self.AvgPiecesStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.AvgPPSName.setText(_translate("NullpoTracker", "Avg PPS:"))
        self.AvgPPSStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.AvgScoreName.setText(_translate("NullpoTracker", "Avg Score:"))
        self.AvgScoreStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.HighestLinesName.setText(
            _translate("NullpoTracker", "Highest Lines:"))
        self.HighestLinesStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.LowestLinesName.setText(
            _translate("NullpoTracker", "Lowest Lines:"))
        self.LowestLinesStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.HighestPiecesName.setText(
            _translate("NullpoTracker", "Highest Pieces:"))
        self.HighestPiecesStat.setText(
            _translate("NullpoTracker", "TextLabel"))
        self.LowestPiecesName.setText(
            _translate("NullpoTracker", "Lowest Pieces:"))
        self.LowestPiecesStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.HighestPPSName.setText(
            _translate("NullpoTracker", "Highest PPS:"))
        self.HighestPPSStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.LowestPPSName.setText(_translate("NullpoTracker", "Lowest PPS:"))
        self.LowestPPSStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.HighestTimeName.setText(
            _translate("NullpoTracker", "Highest Time:"))
        self.HighestTimeStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.LowestTimeName.setText(
            _translate("NullpoTracker", "Lowest Time:"))
        self.LowestTimeStat.setText(_translate("NullpoTracker", "TextLabel"))
        self.ExtremaRadioButton.setText(_translate("NullpoTracker", "Extrema"))
        self.PercentileRadioButton.setText(
            _translate("NullpoTracker", "Percentile"))
        self.ModesEnabledLabel.setText(
            _translate("NullpoTracker", "Enabled Modes:"))
        self.DateRangeLabel.setText(_translate("NullpoTracker", "Date Range:"))
        self.FromLabel.setText(_translate("NullpoTracker", "From:"))
        self.ToLabel.setText(_translate("NullpoTracker", "To:"))
        item = self.gameTracker.horizontalHeaderItem(0)
        item.setText(_translate("NullpoTracker", ""))
        item = self.gameTracker.horizontalHeaderItem(1)
        item.setText(_translate("NullpoTracker", "Name"))
        item = self.gameTracker.horizontalHeaderItem(2)
        item.setText(_translate("NullpoTracker", "Mode"))
        item = self.gameTracker.horizontalHeaderItem(3)
        item.setText(_translate("NullpoTracker", "PPS"))
        item = self.gameTracker.horizontalHeaderItem(4)
        item.setText(_translate("NullpoTracker", "Time (s)"))
        item = self.gameTracker.horizontalHeaderItem(5)
        item.setText(_translate("NullpoTracker", "Score"))
        item = self.gameTracker.horizontalHeaderItem(6)
        item.setText(_translate("NullpoTracker", "Pieces"))
        item = self.gameTracker.horizontalHeaderItem(7)
        item.setText(_translate("NullpoTracker", "Lines"))
        item = self.gameTracker.horizontalHeaderItem(8)
        item.setText(_translate("NullpoTracker", "Goal"))
        self.SelectionLabel.setText(_translate("NullpoTracker", " Selection"))
        self.SelectionPPSName.setText(_translate("NullpoTracker", "PPS:"))
        self.SelectionPPSStat.setText(_translate("NullpoTracker", ""))
        self.SelectionTimeName.setText(_translate("NullpoTracker", "Time:"))
        self.SelectionTimeStat.setText(
            _translate("NullpoTracker", ""))
        self.SelectionScoreGoalName.setText(
            _translate("NullpoTracker", "Score:"))
        self.SelectionScoreGoalStat.setText(
            _translate("NullpoTracker", ""))
        self.SelectionLinesName.setText(_translate("NullpoTracker", "Lines:"))
        self.SelectionLinesStat.setText(
            _translate("NullpoTracker", ""))
        self.SelectionPiecesName.setText(
            _translate("NullpoTracker", "Pieces:"))
        self.SelectionPiecesStat.setText(
            _translate("NullpoTracker", ""))
        self.SelectionNameName.setText(_translate("NullpoTracker", "Name:"))
        self.SelectionNameStat.setText(
            _translate("NullpoTracker", ""))
        self.SelectionModeName.setText(_translate("NullpoTracker", "Mode:"))
        self.SelectionModeStat.setText(
            _translate("NullpoTracker", ""))
        self.menuMenu.setTitle(_translate("NullpoTracker", "Menu"))
        self.menuButtonRefresh.setText(_translate("NullpoTracker", "Refresh"))
        self.menuButtonExit.setText(_translate("NullpoTracker", "Exit"))
