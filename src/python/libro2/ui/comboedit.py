from PyQt5.QtWidgets import QComboBox

class ComboEditItemAction:
    Keep = '< keep >'
    Blank = '< blank >'


class ComboEdit(QComboBox):
    def __init__(self, parent):
        super(ComboEdit, self).__init__(parent)
        self.setEditable(True)

    def init(self):
        self.clear()
        self.setEditable(True)
        self.addItem(ComboEditItemAction.Keep)
        self.addItem(ComboEditItemAction.Blank)

    def addUserItem(self, text):
        if self.findText(text) == -1:
            self.addItem(text)

    def setInitialIndex(self):
        if self.count() == 3:
            self.setCurrentIndex(2)
        else:
            self.setCurrentIndex(0)

    def getUserText(self, userText):
        if self.currentText() == ComboEditItemAction.Keep:
            return userText
        elif self.currentText() == ComboEditItemAction.Blank:
            return None
        else:
            return self.currentText()
