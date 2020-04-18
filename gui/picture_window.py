# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picture_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_PictureWindow(object):
    def setupUi(self, PictureWindow):
        PictureWindow.setObjectName("PictureWindow")
        PictureWindow.resize(332, 318)
        self.centralwidget = QtWidgets.QWidget(PictureWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.labelPicture = QtWidgets.QLabel(self.centralwidget)
        self.labelPicture.setObjectName("labelPicture")
        self.gridLayout.addWidget(self.labelPicture, 0, 0, 1, 1)
        PictureWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PictureWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 332, 18))
        self.menubar.setObjectName("menubar")
        PictureWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PictureWindow)
        self.statusbar.setObjectName("statusbar")
        PictureWindow.setStatusBar(self.statusbar)

        self.retranslateUi(PictureWindow)
        QtCore.QMetaObject.connectSlotsByName(PictureWindow)

    def retranslateUi(self, PictureWindow):
        _translate = QtCore.QCoreApplication.translate
        PictureWindow.setWindowTitle(_translate("PictureWindow", "NRP-Solver Picture"))
        self.labelPicture.setText(_translate("PictureWindow", "TextLabel"))
