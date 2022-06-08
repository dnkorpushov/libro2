import os
import sys
import subprocess
import webbrowser
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from .convertdialog_ui import Ui_ConvertDialog


class ConvertDialog(QDialog, Ui_ConvertDialog):
    def __init__(self, parent):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)

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

    @overwrite.setter
    def overwrite(self, value):
        self.checkOverwrite.setChecked(value)

    @converterPath.setter
    def converterPath(self, value):
        self.textConverterPath.setText(value)

    @converterConfig.setter
    def converterConfig(self, value):
        self.textConverterConfig.setText(value)

    def accept(self):
        if self.outputPath:
            if not os.path.exists(self.outputPath):
                QMessageBox.critical(self,
                                     'Libro2', 
                                     'Folder "{0}" not exsist'.format(self.outputPath))
                return False
        else:
            QMessageBox.critical(self, 'Libro2', 'Output folder not specified')
            return False
                
        if self.converterPath:
            if not os.path.exists(self.converterPath):
                QMessageBox.critical(self, 
                                     'Libro2', 
                                     'File "{0}" not exsist'.format(self.converterPath))
                return False
        else:
            QMessageBox.critical(self, 'Libro2', 'Path to fb2converter not specified')
            return False

        if self.converterConfig:
            if not os.path.exists(self.converterConfig):
                QMessageBox.critical(self, 
                                     'Libro2', 
                                     'File "{0}" not exsist'.format(self.converterConfig))
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
        result = QFileDialog.getExistingDirectory(self, caption='Select output folder')
        if result:
            self.textOutputDir.setText(result)

    def onToolConverterPath(self):
        result = QFileDialog.getOpenFileName(self, 
                                             caption='Select fb2c executable',
                                             filter='Executable files (*.exe);;All files (*.*)')
        if result:
            self.textConverterPath.setText(result[0])

    def onToolConverterConfig(self):
        result = QFileDialog.getOpenFileName(self,
                                             caption='Select fb2c config file',
                                             filter='Config files (*.json *.yaml *.yml *.toml);;All files(*.*)')
        if result:
            self.textConverterConfig.setText(result[0])
