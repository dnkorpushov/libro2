import os
import sys
import webbrowser
import subprocess

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication, QSize

from .settingsdialog_ui import Ui_SettingsDialog

_t = QCoreApplication.translate


class SettingsDialog(Ui_SettingsDialog, QDialog):
    def __init__(self, parent, scale_factor=1):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        base_width = 520 
        base_height = 275 

        self.setMinimumSize(QSize(int(base_width * scale_factor), int(base_height * scale_factor)))  
        self.resize(self.minimumSize())
        self.adjustSize()

        self.checkOpenFolderOnStart.clicked.connect(self.onOpenFolderOnStartClick)
        self.btnEditConfig.clicked.connect(self.onEditConfig)
        self.btnDowloadConverter.clicked.connect(self.onDownloadConverter)

        if sys.platform == 'win32':
            self.textConverterPath.setFilter(_t('cv', 'fb2c.exe (fb2c.exe);;All files (*.*)'))
        else:
            self.textConverterPath.setFilter(_t('cv', 'fb2c (fb2c);;All files (*)'))

        self.textConverterPath.setCaption(_t('cv', 'Select fb2c executable'))
        self.textConverterConfig.setCaption(_t('cv', 'Select fb2c config file'))
        self.textConverterConfig.setFilter(_t('cv', 'Config files (*.json *.yaml *.yml *.toml);;All files(*.*)'))


    @property
    def isOpenFolderOnStart(self):
        return self.checkOpenFolderOnStart.isChecked()

    @property
    def openFolderOnStart(self):
        return self.textOpenFolderOnStart.text()

    @property
    def converterPath(self):
        return self.textConverterPath.text()

    @property
    def converterConfig(self):
        return self.textConverterConfig.text()

    @isOpenFolderOnStart.setter
    def isOpenFolderOnStart(self, value):
        self.checkOpenFolderOnStart.setChecked(value)
        self.textOpenFolderOnStart.setEnabled(value)

    @openFolderOnStart.setter
    def openFolderOnStart(self, value):
        self.textOpenFolderOnStart.setText(value)
    
    @converterPath.setter
    def converterPath(self, value):
        self.textConverterPath.setText(value)

    @converterConfig.setter
    def converterConfig(self, value):
        self.textConverterConfig.setText(value)

    def onOpenFolderOnStartClick(self):
        self.textOpenFolderOnStart.setEnabled(self.checkOpenFolderOnStart.isChecked())
    
    def onEditConfig(self):
        if self.converterConfig:
            if sys.platform == 'win32':
                os.startfile(self.converterConfig)
            elif sys.platform == 'darwin':
                subprocess.call(('open', self.converterConfig))
            else:
                subprocess.call(('xdg-open', self.converterConfig))

    def onDownloadConverter(self):
        link = 'https://github.com/rupor-github/fb2converter/releases/'
        browser = webbrowser.get()
        browser.open_new_tab(link)
