from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QCoreApplication

_t = QCoreApplication.translate



class ComboEdit(QComboBox):
    def __init__(self, parent):
        super(ComboEdit, self).__init__(parent)
        self.setEditable(True)

        self.Keep = _t('info', '< keep >')
        self.Blank = _t('info', '< blank >')

    def init(self):
       
        self.clear()
        self.setEditable(True)
        self.addItem(self.Keep)
        self.addItem(self.Blank)

    def addUserItem(self, text):
        if self.findText(text) == -1:
            self.addItem(text)

    def setInitialIndex(self):
        if self.count() == 3:
            self.setCurrentIndex(2)
        else:
            self.setCurrentIndex(0)

    def getUserText(self, userText):
        if self.currentText() == self.Keep:
            return userText
        elif self.currentText() == self.Blank:
            return None
        else:
            return self.currentText()
