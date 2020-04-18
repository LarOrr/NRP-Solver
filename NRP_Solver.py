from PyQt5.QtGui import QCursor
import os
import sys
from typing import List
import PyQt5
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThreadPool, pyqtSlot, QRunnable
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QApplication, QProgressDialog, QDesktopWidget, QTableWidgetItem, \
    QAbstractItemView
from platypus import NSGAII, Problem, Solution, nondominated, AbstractGeneticAlgorithm, GAOperator, HUX, \
    BitFlip, TournamentSelector
from gui import main, result_window, picture_window
from nrp_logic.algorithms import NSGAII_Repair, Repairer
from nrp_logic.entities import NRPInstance, NRPSolution, plot_solutions
from nrp_logic.problems import NRP_Problem_MO, NRP_Problem_SO, make_solutions
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


class Window:
    def show_simple_error(self, text: str):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(text)
        msg.exec_()


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow, Window):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.is_last_single = False
        self.threadpool = QThreadPool()
        self.result = None
        self.nrp_instance = None
        self.btnBrowseFiles.clicked.connect(self.browse_folder)
        self.btnRunSolver.clicked.connect(self.run_algorithm)
        self.btnShowResults.setDisabled(True)
        self.btnShowResults.clicked.connect(self.show_result_window)
        self.actionAbout.triggered.connect(self.show_about)

    def run_algorithm(self):
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
            self.nrp_instance: NRPInstance = reader.read_nrp_instance(filename=file_path)
        except RuntimeError as ex:
            # If cycle
            self.show_file_error(ex, str(ex))
            return
        except Exception as ex:
            self.show_file_error(ex)
            return
        # Multi or Single
        nrp_problem: Problem = None
        self.is_last_single = not self.radioMulti.isChecked()
        if self.radioMulti.isChecked():
            nrp_problem = NRP_Problem_MO(self.nrp_instance)
        else:
            nrp_problem = NRP_Problem_SO(self.nrp_instance)

        algorithm: AbstractGeneticAlgorithm = None
        # TODO Move somewhere and add config
        # Crossover probability is 0.9 and mutation probability = 1 / (size of binary vector)
        variator = None
        # TODO single-point crossover?
        variator = GAOperator(HUX(probability=0.8), BitFlip(probability=1))
        selector = TournamentSelector(5)
        #  Dep or without dep
        if self.radioDependYes.isChecked():
            # TODO fix req for rep
            algorithm = NSGAII_Repair(nrp_problem, repairer=Repairer(self.nrp_instance.requirements), variator=variator,
                                      selector=selector)
        else:
            algorithm = NSGAII(nrp_problem, variator=variator, selector=selector)
        #  Take n runs
        try:
            nruns = int(self.lineNumOfRuns.text())
            if nruns < 1 or nruns > 10000000:
                self.show_simple_error("Number of runs must be between 1 and 10000000!")
                return
        except ValueError:
            self.show_simple_error("Number of runs must be integer!")
            return

        # TODO fix this
        def run_and_back():
            algorithm.run(nruns)
            print(len(algorithm.result))
            solutions: List[Solution] = nondominated(algorithm.result)
            solutions = [sol for sol in solutions if sol.feasible]
            print(len(solutions))

            result: List[NRPSolution] = make_solutions(self.nrp_instance, solutions)
            # Sorting for 2 objectives First maximize score and then minimize cost
            result = sorted(result, key=lambda x: x.total_score, reverse=True)
            if self.is_last_single:
                result = sorted(result, key=lambda x: x.total_cost)
                # Taking only solution with minimal cost
                result = [result[0]]
            self.result = result
            #  TODO separate method
            self.view.hide()
            QApplication.restoreOverrideCursor()
            self.setDisabled(False)
            self.btnShowResults.setDisabled(False)
            self.btnShowResults.setStyleSheet("background-color: lime")

        def set_view(view):
            view.show()
            self.view = view
            resolution = QDesktopWidget().screenGeometry()
            view.move((resolution.width() / 2) - (view.frameSize().width() / 2),
                      (resolution.height() / 2) - (view.frameSize().height() / 2))

        wait = QProgressDialog('Please, wait for algorithm execution...', None, 0, 0)
        wait.setWindowTitle('Status')
        set_view(wait)
        self.setDisabled(True)
        QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
        worker = Worker(run_and_back)
        self.threadpool.start(worker)

    def show_file_error(self, ex: Exception, message: str = "Format of file is incorrect."):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setInformativeText("Please, try to check the correctness of the file and the chosen file format")
        msg.setWindowTitle("File reading error")
        msg.setDetailedText("Additional information about problem:\n{}".format(ex))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def browse_folder(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Choose file with NRP instance")
        self.lineFilePath.setText(path)

    def show_about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('Next Release Problem (NRP) Solver v 1.0')
        msg.setInformativeText('Developer:\n'
                               'Illarion Oralin\n'
                               'HSE University, Faculty of Computer Science\n'
                               'Software Engineering, 3rd year\n'
                               '\n2020')
        msg.setWindowTitle("NRP Solver About")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_result_window(self):
        if self.result is None:
            self.show_simple_error('You have to run the algorithm first!')
            return
        elif len(self.result) == 0:
            self.show_simple_error("0 solution found! Please try to run algorithm with bigger run number!")
            return
        ResultWindow(self, self.result, self.nrp_instance).show()


# --------------------------------------------------------------------------------------------
class ResultWindow(QtWidgets.QMainWindow, result_window.Ui_ResultWindow, Window):
    def __init__(self, parent, result: List[NRPSolution], nrp_instance: NRPInstance):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.resize(700, 500)
        self.result: List[NRPSolution] = result
        self.close()
        self.nrp_instance = nrp_instance
        self.labelTotalInfo.setText("Budget = {} || Total cost of all req. = {} || Total score of all req. = {} "
                                    .format(round(nrp_instance.budget, 2), round(nrp_instance.total_cost, 2),
                                            round(nrp_instance.total_score, 2)))
        self.labels = ['Total Score', 'Total Cost', 'List of requirements']
        self.fill_table()
        # TODO save img
        self.checkSaveImg.hide()
        self.btnSaveResult.clicked.connect(self.save_result)
        self.btnVisualize.clicked.connect(self.show_visualisation)

    def fill_table(self):
        table = self.tableResult
        table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        table.setColumnCount(len(self.labels))
        table.setRowCount(len(self.result))
        table.setHorizontalHeaderLabels(self.labels)
        # Resize to content
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setDefaultAlignment(QtCore.Qt.AlignLeft)
        # table.horizontalHeader().setStretchLastSection(True)
        table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        for i, sol in enumerate(self.result):
            table.setItem(i, 0, QTableWidgetItem(str(sol.total_score)))
            table.setItem(i, 1, QTableWidgetItem(str(sol.total_cost)))
            table.setItem(i, 2, QTableWidgetItem(sol.reqs_to_string(' | ')))

    def show_visualisation(self):
        img_name = plot_solutions(self.result, self.nrp_instance.budget, 'Solutions')
        PictureWindow(self, img_name).show()

    def save_result(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save result to .csv", 'result.csv', '.csv')
        if path is None or path == '':
            return
        try:
            dirname = os.path.dirname(path)
            filename = os.path.splitext(path)[0]
            wfile = open(path, 'w+')
            wfile.write(';'.join(self.labels) + '\n')
            for sol in self.result:
                wfile.write(';'.join([str(sol.total_score), str(sol.total_score), sol.reqs_to_string(' | ')]) + '\n')
            # if self.checkSaveImg.isChecked():
            #     cur = pathlib.Path().absolute()
            #     img_save_path = '{}{}.png'.format(dirname, filename)
            #     img_save_path = relpath(cur, img_save_path)
            #     print(img_save_path)
            #     img_src = plot_solutions(self.result, self.nrp_instance.budget, 'Solutions', img_save_path)
            # copyfile(img_src, img_save_path)
            # plot_solutions(self.result, self.nrp_instance.budget, 'Solutions', 'temp2.png')
        except Exception as ex:
            self.show_simple_error('Something wrong with chosen file save path!\nPlease try to choose another!')


class PictureWindow(QtWidgets.QMainWindow, picture_window.Ui_PictureWindow):

    def __init__(self, parent, image_path):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.image_path = image_path
        self.show_picture()

    def show_picture(self):
        # Create widget
        label = self.labelPicture
        pixmap = PyQt5.QtGui.QPixmap(self.image_path)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
