from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from .processdialog_ui import Ui_ProcessDialog
import ebookmeta
import database


class Worker(QObject):
    currentProcess = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, files, parent=None):
        super(Worker, self).__init__(parent)
        self.files = files
        self.isRunning = True
        self.errors = []
        self.metadata = []

    def loadFiles(self):
        i = 0
        count = len(self.files)
        for file in self.files:
            if self.isRunning:
                i += 1
                try:
                    meta = ebookmeta.get_metadata(file)
                    self.metadata.append(meta)
                    database.add_book(file)
                    self.currentProcess.emit(i, count)
                except Exception as e:
                    print(e)

            else:
                self.metadata.clear()
                break
        self.finished.emit()

    def kill(self):
        self.isRunning = False


class AddFilesDialog(QDialog, Ui_ProcessDialog):
    def __init__(self, parent, files):
        super(AddFilesDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Add files')

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.progressBar.setMaximum(len(files))
        self.progressBar.setMinimum(0)
        self.progressLabel.setText('')

        self.thread = QThread()
        self.worker = Worker(files)
        self.worker.currentProcess.connect(self.setCurrentProcess)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)

        self.thread.started.connect(self.worker.loadFiles)
        self.thread.finished.connect(self.close)


    def setCurrentProcess(self, index, count):
        self.progressLabel.setText('Add files... {0} of {1}'.format(index, count))
        self.progressBar.setValue(index)


    def cancelProcess(self):    
        self.worker.kill()


    def getMetadata(self):
        return self.worker.metadata


    def showEvent(self, event):
        self.thread.start()