import os

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication, QSize
from .convertdialog_ui import Ui_ConvertDialog

_t = QCoreApplication.translate

class ConvertDialog(QDialog, Ui_ConvertDialog):
    def __init__(self, parent, scale_factor=1):
        super(ConvertDialog, self).__init__(parent)
        self.setupUi(self)

        base_width = 450 
        base_height = 270 

        self.setMinimumSize(QSize(int(base_width * scale_factor), int(base_height * scale_factor)))  
        self.resize(self.minimumSize())

        self.comboFormat.currentIndexChanged.connect(self.onFormatChanged)

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
                
        return super().accept()

