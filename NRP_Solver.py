import math
import sys
import threading
from contextlib import contextmanager
from typing import List

from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtCore import QThreadPool, pyqtSlot, QRunnable
from PyQt5.QtGui import QCursor, QPalette, QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QProgressDialog, QDesktopWidget
from PyQt5.uic.properties import QtGui
from platypus import NSGAII, Problem, Solution, nondominated, AbstractGeneticAlgorithm

from gui import main
from nrp_logic.algorithms import NSGAII_Repair, Repairer
from nrp_logic.entities import NRPInstance
from nrp_logic.nrp import NRP_Problem_MO, NRP_Problem_SO
from util.file_reader import AbstractFileReader, ClassicFileReader, FileReader


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.fn(*self.args, **self.kwargs)


# @contextmanager
# def wait_cursor():
#     try:
#         QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
#         yield
#     finally:
#         QApplication.restoreOverrideCursor()


# class Overlay(QWidget):
#
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         palette = QPalette(self.palette())
#         palette.setColor(palette.Background, QtCore.Qt.transparent)
#         self.setPalette(palette)
#
#     def paintEvent(self, event):
#
#         painter = QPainter()
#         painter.begin(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
#         painter.setPen(QPen(QtCore.Qt.NoPen))
#
#         for i in range(6):
#             if (self.counter / 5) % 6 == i:
#                 painter.setBrush(QBrush(QColor(127 + (self.counter % 5) * 32, 127, 127)))
#             else:
#                 painter.setBrush(QBrush(QColor(127, 127, 127)))
#             painter.drawEllipse(
#                 self.width() / 2 + 30 * math.cos(2 * math.pi * i / 6.0) - 10,
#                 self.height() / 2 + 30 * math.sin(2 * math.pi * i / 6.0) - 10,
#                 20, 20)
#
#         painter.end()
#
#     def showEvent(self, event):
#
#         self.timer = self.startTimer(50)
#         self.counter = 0
#
#     def timerEvent(self, event):
#         self.counter += 1
#         self.update()
#         if self.counter == 60:
#             self.killTimer(self.timer)
#             self.hide()


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.setupUi(self)
        self.btnBrowseFiles.clicked.connect(self.browse_folder)
        self.btnRunSolver.clicked.connect(self.run_algorithm)

    def run_algorithm(self):
        self.lineFilePath.setText('C:/Users/Lar/Documents/Study/CouseWork-3/PyProgramNRP/test_data/classic/nrp3.txt')
        # self.radioClassicFormat.setChecked()

        file_path = self.lineFilePath.text()
        if file_path == "":
            self.show_simple_error("Please choose file!")
            return
        print(file_path)
        # Reading file to NRP instance
        reader: AbstractFileReader = None
        if self.radioClassicFormat.isChecked():
            reader = ClassicFileReader()
        else:
            reader = FileReader()
        try:
            nrp_instance: NRPInstance = reader.read_nrp_instance(filename=file_path)
        except Exception as ex:
            self.show_file_error(ex)
            return
        # Multi or Single
        nrp_problem: Problem = None
        if self.radioMulti.isChecked():
            nrp_problem = NRP_Problem_MO(nrp_instance)
        else:
            nrp_problem = NRP_Problem_SO(nrp_instance)

        algorithm: AbstractGeneticAlgorithm = None
        #  Dep or without dep
        if self.radioDependYes.isChecked():
            # TODO fix req for rep
            algorithm = NSGAII_Repair(nrp_problem, repairer=Repairer(nrp_instance.requirements))
        else:
            algorithm = NSGAII(nrp_problem)
        #  Take n runs
        try:
            nruns = int(self.lineNumOfRuns.text())
        except ValueError:
            self.show_simple_error("Number of runs must be integer!")
            return
        # t = threading.Thread()
        # msg = QMessageBox()
        # msg.setText("Please wait to connect to the server.")
        # msg.setWindowTitle("Checking for update.")
        # msg.exec_()
        # print("Start!")
        # self.setOverrideCursor(Qt.WaitCursor)
        # self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # self.overlay = Overlay(self.centralWidget())
        # self.overlay.show()
        # algorithm.run(nruns)
        # self.overlay.hide()
        # self.btnRunSolver.blockSignals()
        # button.clicked.connect(self.overlay.show)
        def run_and_back():
            algorithm.run(nruns)
            # print("Done!")
            # algorithm.run(nruns)
            # self.threadpool.start()
            # msg.done(0)
            print(len(algorithm.result))
            solutions: List[Solution] = nondominated(algorithm.result)
            solutions = [sol for sol in solutions if sol.feasible]
            print(len(solutions))
            # self.progressBar.
            self.result = sorted(solutions, key=lambda x: x.objectives[0], reverse=True)
            # progress.hide()
            self.view.hide()
            QApplication.restoreOverrideCursor()
            self.setDisabled(False)

            # with wait_cursor():
        #     self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
            # self.setDisabled(True)
        #
        def set_view(view):
            # if not self.view hasattr(self, 'view'):
            #     self.view.hide()
            view.show()
            self.view = view

            resolution = QDesktopWidget().screenGeometry()
            view.move((resolution.width() / 2) - (view.frameSize().width() / 2),
                      (resolution.height() / 2) - (view.frameSize().height() / 2))
        wait = QProgressDialog('Please, wait for algorithm execution...', None, 0, 0)
        wait.setWindowTitle(' ')
        set_view(wait)

        self.setDisabled(True)
        QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
        worker = Worker(run_and_back)
        # worker.finished.connect(run_and_back())
        self.threadpool.start(worker)

        # self.threadpool.waitForDone()
        # self.setDisabled(False)
            # algorithm.run(nruns)

            # self.threadpool.thread().wait()
        # self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

        # print(algorithm.nfe)
        # worker = Worker(algorithm.run, nruns)
        # self.threadpool.start(worker)
        # while len(algorithm.result) == 0:
        #     print(algorithm.nfe)
        #     self.progressBar.setValue(algorithm.nfe / nruns)
        # i = 0
        # algorithm.
        # print("Done!")
        # # algorithm.run(nruns)
        # # self.threadpool.start()
        # # msg.done(0)
        # print(len(algorithm.result))
        # solutions: List[Solution] = nondominated(algorithm.result)
        # solutions = [sol for sol in solutions if sol.feasible]
        # print(len(solutions))
        # # self.progressBar.
        # result = sorted(solutions, key=lambda x: x.objectives[0], reverse=True)

    def show_simple_error(self, text: str):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.exec_()

    def show_file_error(self, ex: Exception):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Format of file is incorrect.")
        msg.setInformativeText("Please, try to check the correctness of the file and the chosen file format")
        msg.setWindowTitle("File reading error")
        msg.setDetailedText("Additional information about problem:\n{}".format(ex))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        # msg.buttonClicked.connect(msgbtn)

    def browse_folder(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file with NRP instance")
        self.lineFilePath.setText(path)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
