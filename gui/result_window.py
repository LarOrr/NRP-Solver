# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow):
        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.resize(417, 308)
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnVisualize = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnVisualize.setFont(font)
        self.btnVisualize.setObjectName("btnVisualize")
        self.horizontalLayout.addWidget(self.btnVisualize)
        spacerItem = QtWidgets.QSpacerItem(168, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkSaveImg = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.checkSaveImg.setFont(font)
        self.checkSaveImg.setObjectName("checkSaveImg")
        self.horizontalLayout.addWidget(self.checkSaveImg)
        self.btnSaveResult = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnSaveResult.setFont(font)
        self.btnSaveResult.setObjectName("btnSaveResult")
        self.horizontalLayout.addWidget(self.btnSaveResult)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelTotalInfo = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelTotalInfo.setFont(font)
        self.labelTotalInfo.setObjectName("labelTotalInfo")
        self.verticalLayout.addWidget(self.labelTotalInfo)
        self.labelSolution = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.labelSolution.setFont(font)
        self.labelSolution.setObjectName("labelSolution")
        self.verticalLayout.addWidget(self.labelSolution)
        self.tableResult = QtWidgets.QTableWidget(self.centralwidget)
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.verticalLayout.addWidget(self.tableResult)
        ResultWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 18))
        self.menubar.setObjectName("menubar")
        ResultWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultWindow)
        self.statusbar.setObjectName("statusbar")
        ResultWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ResultWindow)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi(self, ResultWindow):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "NRP Solver - Result"))
        self.btnVisualize.setText(_translate("ResultWindow", "Visualize Result"))
        self.checkSaveImg.setText(_translate("ResultWindow", "Save with image"))
        self.btnSaveResult.setText(_translate("ResultWindow", "Save result to .csv"))
        self.labelTotalInfo.setText(_translate("ResultWindow", "Budget = {} || Total cost = {} || Total score = {} "))
        self.labelSolution.setText(_translate("ResultWindow", "Found solutions:"))
