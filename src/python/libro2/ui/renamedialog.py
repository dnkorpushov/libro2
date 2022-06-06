from PyQt5.QtWidgets import QDialog

from .renamedialog_ui import Ui_RenameDialog


class RenameDialog(Ui_RenameDialog, QDialog):
    def __init__(self, parent):
        super(RenameDialog, self).__init__(parent)
        self.setupUi(self)
        self._book_list = []

        self.textAuthorFormat.lineEdit().textChanged.connect(self.generateSample)
        self.textFilenameFormat.lineEdit().textChanged.connect(self.generateSample)

    @property
    def authorFormat(self):
        return self.textAuthorFormat.currentText()

    @property
    def filenameFormat(self):
        return self.textFilenameFormat.currentText()

    @property
    def bookList(self):
        return self._book_list

    @authorFormat.setter
    def authorFormat(self, value):
        self.textAuthorFormat.setCurrentText(value)

    @filenameFormat.setter
    def filenameFormat(self, value):
        self.textFilenameFormat.setCurrentText(value)

    @bookList.setter
    def bookList(self, value):
        self.generateSample()
        self._book_list = value

    def generateSample(self):
        for book in self._book_list:
            self.labelSample.setText(book['title'])
            break




