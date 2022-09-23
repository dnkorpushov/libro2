import traceback
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt, QCoreApplication
from .processdialog_ui import Ui_ProcessDialog
from .smartdialog import SmartDialog
import ebookmeta
import database

_t = QCoreApplication.translate

class Worker(QObject):
    currentProcess = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, files, parent=None):
        super(Worker, self).__init__(parent)
        self.files = files
        self.isRunning = True
        self.errors = []

    def loadFiles(self):
        i = 0
        count = len(self.files)
        for file in self.files:
            if self.isRunning:
                i += 1
                if file.lower().endswith('.fb2') or file.lower().endswith('.fb2.zip') or file.lower().endswith('.epub'):
                    try:
                        database.add_book(file)
                        self.currentProcess.emit(i, count)

                    except ebookmeta.UnknownFormatException:
                        self.errors.append({'src': file, 'dest': None, 'error': _t('add', 'Unknown file format.')})

                    except Exception as e:
                        trace = traceback.format_exc()
                        self.errors.append({'src': file, 'dest': None, 'error': trace})
            else:
                self.errors.append({'src': None, 'dest': None, 'error': _t('add', 'User interrupt')})                
                break
        self.finished.emit()

    def kill(self):
        self.isRunning = False


class AddFilesDialog(SmartDialog, Ui_ProcessDialog):
    def __init__(self, parent, files):
        super(AddFilesDialog, self).__init__(parent)
        self.setupUi(self)

        self.restoreSize()

        self.setWindowTitle(_t('add','Add files'))

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
        self.progressLabel.setText(_t('add','Add files... {0} of {1}').format(index, count))
        self.progressBar.setValue(index)

    def cancelProcess(self):    
        self.worker.kill()

    def showEvent(self, event):
        self.thread.start()

    def getErrors(self):
        return self.worker.errors

    def _save_size(self):
        return
