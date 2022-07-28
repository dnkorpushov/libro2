
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QCoreApplication
from .editdialog_ui import Ui_EditDialog

_t = QCoreApplication.translate

class EditDialog(QDialog, Ui_EditDialog):
    def __init__(self, parent):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)



