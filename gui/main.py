# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(402, 311)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioCommonFormat = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioCommonFormat.setChecked(True)
        self.radioCommonFormat.setObjectName("radioCommonFormat")
        self.horizontalLayout_5.addWidget(self.radioCommonFormat)
        self.radioClassicFormat = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioClassicFormat.setObjectName("radioClassicFormat")
        self.horizontalLayout_5.addWidget(self.radioClassicFormat)
        self.verticalLayout.addWidget(self.groupBox_5)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineFilePath = QtWidgets.QLineEdit(self.groupBox)
        self.lineFilePath.setObjectName("lineFilePath")
        self.horizontalLayout.addWidget(self.lineFilePath)
        self.btnBrowseFiles = QtWidgets.QPushButton(self.groupBox)
        self.btnBrowseFiles.setObjectName("btnBrowseFiles")
        self.horizontalLayout.addWidget(self.btnBrowseFiles)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStatusTip("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioSingle = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioSingle.setChecked(True)
        self.radioSingle.setObjectName("radioSingle")
        self.horizontalLayout_2.addWidget(self.radioSingle)
        self.radioMulti = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioMulti.setObjectName("radioMulti")
        self.horizontalLayout_2.addWidget(self.radioMulti)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioDependYes = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioDependYes.setChecked(True)
        self.radioDependYes.setObjectName("radioDependYes")
        self.horizontalLayout_3.addWidget(self.radioDependYes)
        self.radioDependNo = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioDependNo.setObjectName("radioDependNo")
        self.horizontalLayout_3.addWidget(self.radioDependNo)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setToolTipDuration(30000)
        self.label.setStatusTip("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.lineNumOfRuns = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineNumOfRuns.setObjectName("lineNumOfRuns")
        self.verticalLayout_2.addWidget(self.lineNumOfRuns)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnShowResults = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnShowResults.setFont(font)
        self.btnShowResults.setAutoFillBackground(False)
        self.btnShowResults.setCheckable(False)
        self.btnShowResults.setObjectName("btnShowResults")
        self.horizontalLayout_4.addWidget(self.btnShowResults)
        self.btnRunSolver = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btnRunSolver.setFont(font)
        self.btnRunSolver.setObjectName("btnRunSolver")
        self.horizontalLayout_4.addWidget(self.btnRunSolver)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 402, 18))
        self.menubar.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuMenu.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NRP Solver"))
        self.groupBox_5.setTitle(_translate("MainWindow", "File format"))
        self.radioCommonFormat.setText(_translate("MainWindow", "Common format"))
        self.radioClassicFormat.setText(_translate("MainWindow", "Classic format"))
        self.groupBox.setTitle(_translate("MainWindow", "Choose file with NRP instance"))
        self.btnBrowseFiles.setText(_translate("MainWindow", "Browse"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Select multi-objective or single-objective"))
        self.radioSingle.setText(_translate("MainWindow", "Single (Maximize score)"))
        self.radioMulti.setText(_translate("MainWindow", "Multi (Maximize score and minimize cost)"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Use dependencies between requirements?"))
        self.radioDependYes.setText(_translate("MainWindow", "Yes"))
        self.radioDependNo.setText(_translate("MainWindow", "No"))
        self.label.setText(_translate("MainWindow",
                                      "Number of runs (more runs mean better accuracy but takes more time to execute) : "))
        self.lineNumOfRuns.setText(_translate("MainWindow", "10000"))
        self.btnShowResults.setText(_translate("MainWindow", "Show results"))
        self.btnRunSolver.setText(_translate("MainWindow", "Run Solver"))
        self.menuMenu.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
