import sys
from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt


def _icon(pixmap):
    icon = QIcon(pixmap)
    icon.addPixmap(pixmap, QIcon.Disabled)
    return icon

class MainToolbar(QToolBar):
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
    
        self.savePixmap = None
        self.addPixmap = None
        self.folderPixmap = None
        self.renamePixmap = None
        self.convertPixmap = None

    def addSeparator(self):
        if sys.platform == 'win32':
            separator = QWidget(self)
            separator.setFixedWidth(4)
            self.addWidget(separator)

    def setCenterAlign(self):
        spacer1 = QWidget()
        spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        for action in self.actions():
            self.insertWidget(action, spacer1)
            break
        self.addWidget(spacer2)

    def setLargeIcons(self):
        self.savePixmap = QPixmap(':/toolbar/save_28px.png')
        self.addPixmap = QPixmap(':/toolbar/add_28px.png')
        self.folderPixmap = QPixmap(':/toolbar/folder_28px.png')
        self.renamePixmap = QPixmap(':/toolbar/edit_28px.png')
        self.convertPixmap = QPixmap(':/toolbar/convert_28px.png')
       
        if sys.platform == 'win32':
            self.setIconSize(QSize(36, 36))
        else:
            self.setIconSize(QSize(28, 28))
        self.setIcons()

    def setSmallIcons(self):
        self.savePixmap = QPixmap(':/toolbar/save_22px.png')
        self.addPixmap = QPixmap(':/toolbar/add_22px.png')
        self.folderPixmap = QPixmap(':/toolbar/folder_22px.png')
        self.renamePixmap = QPixmap(':/toolbar/edit_22px.png')
        self.convertPixmap = QPixmap(':/toolbar/convert_22px.png')

        if sys.platform == 'win32':
            self.setIconSize(QSize(26, 26))
        else:
            self.setIconSize(QSize(22, 22))
        self.setIcons()

    def setIcons(self):
        for action in self.actions():
            if action.objectName() == 'actionSave_metadata':
                action.setIcon(_icon(self.savePixmap))
            elif action.objectName() == 'actionAdd_file':
                action.setIcon(_icon(self.addPixmap))
            elif action.objectName() == 'actionAdd_folder':
                action.setIcon(_icon(self.folderPixmap))
            elif action.objectName() == 'actionRename':
                action.setIcon(_icon(self.renamePixmap))
            elif action.objectName() == 'actionConvert':
                action.setIcon(_icon(self.convertPixmap))

