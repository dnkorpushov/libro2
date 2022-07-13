import traceback
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from .processdialog_ui import Ui_ProcessDialog
import database
import ebookmeta
import plugin_collection

class Worker(QObject):
    currentProcess = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, plugin, book_info_list):
        super(Worker, self).__init__(None)
        self.book_info_list = book_info_list
        self.plugin = plugin
        self.isRunning = True
        self.errors = []

    def process(self):
        i = 0
        count = len(self.book_info_list)

        for book in self.book_info_list:
            if self.isRunning:
                i += 1
                try:
                    if issubclass(self.plugin.__class__, plugin_collection.MetaPlugin):
                        meta = ebookmeta.get_metadata(book.file)
                        result_meta = self.plugin.perform_operation(meta)
                        if result_meta:
                            ebookmeta.set_metadata(book.file, result_meta)
                            database.update_book_form_metadata(book.id, book.file)
                    
                    elif issubclass(self.plugin.__class__, plugin_collection.FilePlugin):
                        result_file = self.plugin.perform_operation(book.file)
                        if result_file:
                            database.update_filename(book.id, result_file)
                            database.update_book_form_metadata(book.id, result_file)
                    
                except plugin_collection.DebugException as e:
                    self.errors.append({'src': book.file, 'dest': None, 'error': str(e)})

                except Exception as e:
                    self.errors.append({'src': book.file, 'dest': None, 'error': traceback.format_exc()})
                self.currentProcess.emit(i, count)
            else:
                self.errors.append({'src': None, 'dest': None, 'error': 'User interrupt'})
                break
        self.finished.emit()

    def kill(self):
        self.isRunning = False


class RunPluginDialog(QDialog, Ui_ProcessDialog):
    def __init__(self, parent, plugin, book_info_list):
        super(RunPluginDialog, self).__init__(parent)
        self.setupUi(self)
        
        self.operationName = plugin.description()

        self.setWindowTitle(self.operationName)

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.progressBar.setMaximum(len(book_info_list))
        self.progressBar.setMinimum(0)
        self.progressLabel.setText('')

        self.thread = QThread()
        self.worker = Worker(plugin, book_info_list)
        self.worker.currentProcess.connect(self.setCurrentProcess)
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.thread.quit)

        self.thread.started.connect(self.worker.process)
        self.thread.finished.connect(self.close)


    def setCurrentProcess(self, index, count):
        self.progressLabel.setText('Process files... {0} of {1}'.format(index, count))
        self.progressBar.setValue(index)


    def cancelProcess(self):    
        self.worker.kill()


    def getMetadata(self):
        return self.worker.metadata


    def showEvent(self, event):
        self.thread.start()
        
    def getErrors(self):
        return self.worker.errors