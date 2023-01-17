import os
import sys
import webbrowser
import subprocess

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication, QSize

from .settingsdialog_ui import Ui_SettingsDialog
from .smartdialog import SmartDialog

import config

_t = QCoreApplication.translate


class SettingsDialog(Ui_SettingsDialog, SmartDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)

        self.restoreSize()

        self.checkOpenFolderOnStart.clicked.connect(self.onOpenFolderOnStartClick)
        self.btnEditConfig.clicked.connect(self.onEditConfig)
        self.btnDowloadConverter.clicked.connect(self.onDownloadConverter)

        if sys.platform == 'win32':
            self.textConverterPath.setFilter(_t('cv', 'fb2c.exe (fb2c.exe);;All files (*.*)'))
            self.textReaderFb2.setFilter(_t('cv', 'Executable files (*.exe);;All files (*.*)'))
            self.textReaderEpub.setFilter(_t('cv', 'Executable files (*.exe);;All files (*.*)'))
        else:
            self.textConverterPath.setFilter(_t('cv', 'fb2c (fb2c);;All files (*)'))
            self.textReaderFb2.setFilter(_t('cv', 'All files (*)'))
            self.textReaderEpub.setFilter(_t('cv', 'All files (*)'))

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
    def coverImageWidth(self):
        return self.slideCoverImageSize.value()

    @property
    def converterPath(self):
        return self.textConverterPath.text()

    @property
    def converterConfig(self):
        return self.textConverterConfig.text()

    @property
    def readerAppFb2(self):
        return self.textReaderFb2.text()

    @property
    def readerAppEpub(self):
        return self.textReaderEpub.text()

    @isOpenFolderOnStart.setter
    def isOpenFolderOnStart(self, value):
        self.checkOpenFolderOnStart.setChecked(value)
        self.textOpenFolderOnStart.setEnabled(value)

    @openFolderOnStart.setter
    def openFolderOnStart(self, value):
        self.textOpenFolderOnStart.setText(value)
    
    @coverImageWidth.setter
    def coverImageWidth(self, value):
        self.slideCoverImageSize.setValue(value)

    @converterPath.setter
    def converterPath(self, value):
        self.textConverterPath.setText(value)

    @converterConfig.setter
    def converterConfig(self, value):
        self.textConverterConfig.setText(value)

    @readerAppFb2.setter
    def readerAppFb2(self, value):
        self.textReaderFb2.setText(value)

    @readerAppEpub.setter
    def readerAppEpub(self, value):
        self.textReaderEpub.setText(value)

    def onOpenFolderOnStartClick(self):
        self.textOpenFolderOnStart.setEnabled(
            self.checkOpenFolderOnStart.isChecked()
        )

    def onEditConfig(self):
        config_path = config.get_rel_path(self.converterConfig)
        if os.path.exists(config_path):
            if sys.platform == 'win32':
                os.startfile(config_path)
            elif sys.platform == 'darwin':
                subprocess.call(('open', config_path))
            else:
                subprocess.call(('xdg-open', config_path))
        else:
            QMessageBox.critical(
                self,
                'Libro2',
                _t('cv', 'Config file does not exist!')
            )

    def onDownloadConverter(self):
        link = 'https://github.com/rupor-github/fb2converter/releases/'
        browser = webbrowser.get()
        browser.open_new_tab(link)
