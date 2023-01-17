import os

from PyQt5.QtWidgets import QMessageBox, QMenu, QFileDialog
from PyQt5.QtCore import QCoreApplication, QPoint
from .convertdialog_ui import Ui_ConvertDialog
from .smartdialog import SmartDialog

_t = QCoreApplication.translate


class ConvertDialog(SmartDialog, Ui_ConvertDialog):
    def __init__(self, parent):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)

        self.restoreSize()

        self._path_list = set()

        self.comboFormat.currentIndexChanged.connect(self.onFormatChanged)

        self.radioConvertInSourceFolder.clicked.connect(self.setConvertDestionation)
        self.radioConvertTo.clicked.connect(self.setConvertDestionation)
        self.textOutputDir.clicked.connect(self.onTextOutputDirClick)

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
    def debug(self):
        return self.checkDebug.isChecked()

    @property
    def convertPathList(self):
        return list(self._path_list) 

    @property
    def convertInSourceFolder(self):
        return self.radioConvertInSourceFolder.isChecked()

    @convertInSourceFolder.setter
    def convertInSourceFolder(self, value):
        self.radioConvertInSourceFolder.setChecked(value)
        self.radioConvertTo.setChecked(not value)
        self.textOutputDir.setEnabled(not value)

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

    @debug.setter
    def debug(self, value):
        self.checkDebug.setChecked(value)

    @convertPathList.setter
    def convertPathList(self, values):
        if values:
            for val in values:
                self._path_list.add(val)
        
    def onFormatChanged(self):
        self.checkStk.setEnabled(self.comboFormat.currentText() == 'epub')

    def setConvertDestionation(self):
        self.convertInSourceFolder = self.radioConvertInSourceFolder.isChecked()

    def onTextOutputDirClick(self):
        menu = QMenu()
        item = menu.addAction(_t('cv', 'Browse...'))
        item.setData(('browse_action', ''))
        if len(self._path_list) > 0:
            menu.addSeparator()
            pathListMenu = QMenu(_t('cv', 'Saved path list'))
            for p in self._path_list:
                item = pathListMenu.addAction(p)
                item.setData(('saved_path', p))
            menu.addMenu(pathListMenu)
        menu.addSeparator()
        item = menu.addAction(_t('cv', 'Save current path in list'))
        item.setData(('save_action', ''))
        item = menu.addAction(_t('cv', 'Delete current path from list'))
        item.setData(('delete_action', ''))
        
        action = menu.exec_(self.textOutputDir.mapToGlobal(QPoint(self.textOutputDir.width(), 0)))
        if action:
            element = action.data()

            if element[0] == 'browse_action':
                result = QFileDialog.getExistingDirectory(directory=self.textOutputDir.text())
                if result:
                    self.textOutputDir.setText(os.path.normpath(result))
            elif element[0] == 'saved_path':
                self.textOutputDir.setText(element[1])
            elif element[0] == 'save_action':
                if self.textOutputDir.text():
                    self._path_list.add(os.path.normpath(self.textOutputDir.text()))
            elif element[0] == 'delete_action':              
                    self._path_list.discard(os.path.normpath(self.textOutputDir.text()))

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
                
        return super().accept()

