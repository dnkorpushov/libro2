import os
from re import L
from PyQt5.QtWidgets import QWidget,QFileDialog, QPushButton, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import QCoreApplication, pyqtSignal

_t = QCoreApplication.translate


class ClickedLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self):
        self.clicked.emit()

class ButtonLineEdit(QWidget):
    clicked = pyqtSignal()
    textChanged = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.line = QLineEdit()
        self.btn = QPushButton()
        self.btn.clicked.connect(self._onMenuButtonClicked)
        self.line.textChanged.connect(self._onTextChanged)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def setIcon(self, icon):
        self.btn.setIcon(icon)

    def setText(self, text):
        self.line.setText(text)

    def text(self):
        return self.line.text()

    def _onMenuButtonClicked(self):
        self.clicked.emit()
    
    def _onTextChanged(self):
        self.textChanged.emit()
        

    def lineEdit(self):
        return self.line

class FolderPicker(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.line = QLineEdit()
        self.btn = QPushButton()
        
        self.btn.setText(_t('ctl', 'Browse...'))
        

        self.btn.clicked.connect(self._selectFolder)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    def setText(self, text):
        if text:
            self.line.setText(os.path.normpath(text))

    def text(self):
        return self.line.text()

    def setReadOnly(self, readonly):
        self.line.setReadOnly(readonly)

    def isReadOnly(self):
        return self.line.isReadOnly()

    def setEnabled(self, enabled):
        self.line.setEnabled(enabled)
        self.btn.setEnabled(enabled)
    
    def isEnabled(self):
        return self.line.isEnabled()

    def _selectFolder(self):
        result = QFileDialog.getExistingDirectory(directory=self.text())
        if result:
            self.setText(result)

class FilePicker(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.line = QLineEdit()
        self.btn = QPushButton()
        self.btn.setText(_t('ctl', 'Browse...'))
        self.btn.clicked.connect(self._selectFile)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.filter = _t('ctl', 'All files (*.*)')
        self.caption = _t('ctl', 'Open file')

    def setFilter(self, value):
        self.filter = value

    def setCaption(self, value):
        self.caption = value

    def setText(self, text):
        if text:
            self.line.setText(os.path.normpath(text))

    def text(self):
        return self.line.text()

    def setReadOnly(self, readonly):
        self.line.setReadOnly(readonly)

    def isReadOnly(self):
        return self.line.isReadOnly()

    def setEnabled(self, enabled):
        self.line.setEnabled(enabled)
        self.btn.setEnabled(enabled)
    
    def isEnabled(self):
        return self.line.isEnabled()

    def _selectFile(self):
        result = QFileDialog.getOpenFileName(directory=self.text(), filter=self.filter, caption=self.caption)
        if result[0]:
            self.setText(result[0])


