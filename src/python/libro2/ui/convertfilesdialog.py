
import json
import subprocess
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QProcess, QTimer
from .processdialog_ui import Ui_ProcessDialog

def parse_converter_error(b):
    src = None
    dest = None
    error = None

    output = bytes(b).decode()
    strings = output.split('\n')

    # fb2c output string content 4 parts: timestamp, messageType (INFO, WARN or ERROR), text message, JSON attributes

    for s in strings:
        elem = s.split('\t')
        if len(elem) == 4: 
            try:
                info = json.loads(elem[3])
            except:
                pass
            try:
                src = info['source']
            except:
                pass
            try:
                dest = info['to']
            except:
                pass
            if elem[1] in ('ERROR', 'WARN'):
                try:
                    error = info['error']
                except:
                    pass
    
    return {'src': src, 'dest': dest, 'error': error}


class ConvertFilesDialog(QDialog, Ui_ProcessDialog):
    def __init__(self, parent, book_info_list, out_format, out_path, overwrite, converter_path, converter_config):
        super(ConvertFilesDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Convert files')

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.book_info_list = book_info_list
        self.converter_config = converter_config
        self.converter_path = converter_path
        self.overwrite = overwrite
        self.output_format = out_format
        self.output_path = out_path

        self.count = len(book_info_list)
        self.currentIndex = 0
        self.canceled = False
        self.errors = []

        self.process = QProcess()
        self.process.finished.connect(self.endProcess)

        self.progressBar.setMaximum(self.count)
        self.progressBar.setMinimum(0)
        self.progressLabel.setText('')

        self.closeTimer = QTimer(self)
        self.closeTimer.setInterval(200)
        self.closeTimer.timeout.connect(self.onTimerClose)

    def runProcess(self):
        self.setCurrentProcess(self.currentIndex + 1, self.count)

        src = self.book_info_list[self.currentIndex].file
        if src.lower().endswith('.fb2') or  src.lower().endswith('.fb2.zip'):
            args = []
            if self.converter_config:
                args.append('--config')
                args.append(self.converter_config)
            args.append('convert')
            args.append('--to')
            args.append(self.output_format)
            if self.overwrite:
                args.append('--ow')
            args.append(src)
            if self.output_path:
                args.append(self.output_path)
            
            self.process.start(self.converter_path, args)
        else:
            self.errors.append({'src': src, 'dest': None, 'error': 'Epub files not support for conversion'})
            self.currentIndex += 1
            if self.currentIndex < self.count and not self.canceled:
                self.runProcess()
            else:
                self.closeTimer.start() # Hack for close dialog in ShowEvent
        
    def onTimerClose(self):
        self.accept()

    def cancelProcess(self):
        self.errors.append({'src': None, 'dest':None, 'error': 'User interrupt'})
        self.process.kill()
        self.canceled = True

    def endProcess(self, exit_code, exit_status):
        std_output = self.process.readAllStandardOutput()
        err_output = self.process.readAllStandardError()
        error = parse_converter_error(std_output + err_output)
        if error['error']:
            self.errors.append(error)

        self.currentIndex += 1
        
        if self.currentIndex < self.count and not self.canceled:
            self.runProcess()
        else:
            self.accept()

    def setCurrentProcess(self, index, count):
        self.progressLabel.setText('Convert files... {0} of {1}'.format(index, count))
        self.progressBar.setValue(index)

    def showEvent(self, event):
        self.runProcess()
        
