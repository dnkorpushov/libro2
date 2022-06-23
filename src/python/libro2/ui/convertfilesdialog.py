from ast import arg
import os
import shutil
import sys
import json
import tempfile

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QProcess, QTimer, QCoreApplication

from .processdialog_ui import Ui_ProcessDialog

import config
_t = QCoreApplication.translate

def parse_converter_error(b):
    src = None
    dest = None
    error = None

    output = bytes(b).decode()
    strings = output.split('\n')

    # check for global errors
    for s in strings:
        if s.find('*** ERROR ***') >= 0:
            return {'src': src, 'dest': dest, 'error': output}
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
                    if elem[2].lower().find('kindle') >= 0:
                        error = elem[2]
    
    return {'src': src, 'dest': dest, 'error': error}


class ConvertFilesDialog(QDialog, Ui_ProcessDialog):
    def __init__(self, parent, book_info_list, out_format, out_path, overwrite, stk, converter_path, converter_config):
        super(ConvertFilesDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Convert {0} files'.format(len(book_info_list)))

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        self.book_info_list = book_info_list
        self.converter_config = converter_config
        self.converter_path = converter_path
        self.overwrite = overwrite
        self.stk = stk
        self.output_format = out_format
        self.output_path = out_path

        self.count = len(book_info_list)
        self.currentIndex = 0
        self.canceled = False
        self.errors = []
        self.src = None
        self.dest = None
        self.tempfile = None

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

        self.src = os.path.normpath(self.book_info_list[self.currentIndex].file)
        if self.src.lower().endswith(('.fb2', '.fb2.zip')):
            args = []
            if self.converter_config:
                args.append('--config')
                args.append(self.converter_config)
            args.append('convert')
            args.append('--to')
            args.append(self.output_format)
            if self.overwrite:
                args.append('--ow')
            if self.stk and self.output_format == 'epub':
                args.append('--stk')
            args.append(self.src)
            if self.output_path:
                args.append(self.output_path)
            
            self.process.setWorkingDirectory(config.config_path)
            self.process.start(self.converter_path, args)
       
        elif self.src.lower().endswith('.epub') and self.output_format == 'mobi':
            kindlegen = None
            if sys.platform == 'win32':
                kindlegen = os.path.join(os.path.dirname(self.converter_path), 'kindlegen.exe')
            else:
                kindlegen = os.path.join(os.path.dirname(self.converter_path), 'kindlegen')

            tempname = tempfile.NamedTemporaryFile(suffix='.mobi', dir=os.path.dirname(self.src))
            self.tempfile = os.path.normpath(tempname.name)
            self.dest = os.path.normpath(os.path.join(self.output_path, 
                                                      os.path.splitext(os.path.basename(self.src))[0] + '.mobi'))
            
            if os.path.exists(self.dest) and not self.overwrite:
                self.errors.append({'src': self.src, 'dest': None, 'error': _t('cv', 'File {0} exist').format(self.dest)})
                self.next()
            else:
                self.process.start(kindlegen, [self.src, '-o', os.path.basename(self.tempfile)])
        else:
            self.errors.append({ 'src': self.src, 
                                 'dest': None, 'error': 
                                 _t('cv', 'File not support for conversion in {0} format').format(self.output_format)})
            self.next()   

    def next(self):
        self.currentIndex += 1
        if self.currentIndex < self.count and not self.canceled:
            self.runProcess()
        else:
            self.closeTimer.start() # Hack for close dialog in ShowEvent
             
    def onTimerClose(self):
        self.accept()

    def cancelProcess(self):
        self.errors.append({'src': None, 'dest':None, 'error': _t('cv', 'User interrupt')})
        self.process.kill()
        self.canceled = True

    def endProcess(self, exit_code, exit_status):
        std_output = self.process.readAllStandardOutput()
        err_output = self.process.readAllStandardError()

        if self.tempfile and os.path.exists(self.tempfile):
            shutil.move(self.tempfile, self.dest)
        
        self.tempfile = None
        self.src = None
        self.dest = None

        error = parse_converter_error(std_output + err_output)
        if error['error']:
            self.errors.append(error)

        self.currentIndex += 1
        
        if self.currentIndex < self.count and not self.canceled:
            self.runProcess()
        else:
            self.accept()

    def setCurrentProcess(self, index, count):
        self.progressLabel.setText(_t('cv', 'Convert files... {0} of {1}').format(index, count))
        self.progressBar.setValue(index)

    def showEvent(self, event):
        self.runProcess()
        
