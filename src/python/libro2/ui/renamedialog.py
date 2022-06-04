from PyQt5.QtWidgets import QDialog

from .renamedialog_ui import Ui_RenameDialog


class RenameDialog(Ui_RenameDialog, QDialog):
    def __init__(self, parent):
        super(RenameDialog, self).__init__(parent)
        self.setupUi(self)


