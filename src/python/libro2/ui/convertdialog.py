import os
import sys
import subprocess
import webbrowser
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from .convertdialog_ui import Ui_ConvertDialog

_t = QCoreApplication.translate

class ConvertDialog(QDialog, Ui_ConvertDialog):
    def __init__(self, parent):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)
        self.comboFormat.currentIndexChanged.connect(self.onFormatChanged)

        action = self.textOutputDir.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolOutputDir)
        action = self.textConverterPath.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolConverterPath)
        action = self.textConverterConfig.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolConverterConfig)
        
        

    @property
    def outputFormat(self):
        return self.comboFormat.currentText()

    @property
    def outputPath(self):
        return self.textOutputDir.text()

    @property
    def overwrite(self):
        return self.checkOverwrite.isChecked()

    @property
    def stk(self):
        return self.checkStk.isChecked()

    @property
    def converterPath(self):
        return self.textConverterPath.text()

    @property
    def converterConfig(self):
        return self.textConverterConfig.text()

    @outputPath.setter
    def outputPath(self, value):
        self.textOutputDir.setText(value)

    @outputFormat.setter
    def outputFormat(self, value):
        index = self.comboFormat.findText(value)
        if index >= 0:
            self.comboFormat.setCurrentIndex(index)
        self.onFormatChanged()

    @overwrite.setter
    def overwrite(self, value):
        self.checkOverwrite.setChecked(value)

    @stk.setter
    def stk(self, value):
        self.checkStk.setChecked(value)

    @converterPath.setter
    def converterPath(self, value):
        self.textConverterPath.setText(value)

    @converterConfig.setter
    def converterConfig(self, value):
        self.textConverterConfig.setText(value)

    def onFormatChanged(self):
        self.checkStk.setEnabled(self.comboFormat.currentText() == 'epub')

    def accept(self):
        if self.outputPath:
            if not os.path.exists(self.outputPath):
                QMessageBox.critical(self,
                                     'Libro2', 
                                     _t('cv', 'Folder "{0}" not exsist').format(self.outputPath))
                return False
        else:
            QMessageBox.critical(self, 'Libro2', _t('cv', 'Output folder not specified'))
            return False
                
        if self.converterPath:
            if not os.path.exists(self.converterPath):
                QMessageBox.critical(self, 
                                     'Libro2', 
                                     _t('cv', 'File "{0}" not exsist').format(self.converterPath))
                return False
        else:
            QMessageBox.critical(self, 'Libro2', _t('cv', 'Path to fb2converter not specified'))
            return False

        if self.converterConfig:
            if not os.path.exists(self.converterConfig):
                QMessageBox.critical(self, 
                                     'Libro2', 
                                     _t('cv', 'File "{0}" not exsist').format(self.converterConfig))
                return False

        return super().accept()

    def onEditConfig(self,link):
        if self.converterConfig:
            if sys.platform == 'win32':
                os.startfile(self.converterConfig)
            elif sys.platform == 'darwin':
                subprocess.call(('open', self.converterConfig))
            else:
                subprocess.call(('xdg-open', self.converterConfig))

    def onDownloadConverter(self, link):
        browser = webbrowser.get()
        browser.open_new_tab(link)

    def onToolOutputDir(self):
        result = QFileDialog.getExistingDirectory(self, caption=_t('cv', 'Select output folder'))
        if result:
            self.textOutputDir.setText(result)

    def onToolConverterPath(self):
        if sys.platform == 'win32':
            flt = _t('cv', 'fb2c.exe (fb2c.exe);;All files (*.*)')
        else:
            flt = _t('cv', 'fb2c (fb2c);;All files (*)')

        result = QFileDialog.getOpenFileName(self, 
                                             caption=_t('cv', 'Select fb2c executable'),
                                             filter=flt)
        if result:
            self.textConverterPath.setText(result[0])

    def onToolConverterConfig(self):
        result = QFileDialog.getOpenFileName(self,
                                             caption=_t('cv', 'Select fb2c config file'),
                                             filter=_t('cv', 'Config files (*.json *.yaml *.yml *.toml);;All files(*.*)'))
        if result:
            self.textConverterConfig.setText(result[0])
