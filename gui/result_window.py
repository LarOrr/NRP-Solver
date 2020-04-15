# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ResultWindiw(object):
    def setupUi(self, ResultWindiw):
        ResultWindiw.setObjectName("ResultWindiw")
        ResultWindiw.resize(417, 261)
        self.centralwidget = QtWidgets.QWidget(ResultWindiw)
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
        self.tableResult = QtWidgets.QTableWidget(self.centralwidget)
        self.tableResult.setObjectName("tableResult")
        self.tableResult.setColumnCount(0)
        self.tableResult.setRowCount(0)
        self.verticalLayout.addWidget(self.tableResult)
        ResultWindiw.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultWindiw)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 417, 18))
        self.menubar.setObjectName("menubar")
        ResultWindiw.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultWindiw)
        self.statusbar.setObjectName("statusbar")
        ResultWindiw.setStatusBar(self.statusbar)

        self.retranslateUi(ResultWindiw)
        QtCore.QMetaObject.connectSlotsByName(ResultWindiw)

    def retranslateUi(self, ResultWindiw):
        _translate = QtCore.QCoreApplication.translate
        ResultWindiw.setWindowTitle(_translate("ResultWindiw", "NRP Solver - Result"))
        self.btnVisualize.setText(_translate("ResultWindiw", "Visualize Result"))
        self.checkSaveImg.setText(_translate("ResultWindiw", "Save with image"))
        self.btnSaveResult.setText(_translate("ResultWindiw", "Save result"))
