import sys
from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt


class MainToolbar(QToolBar):
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
    
        self.iconSave = None
        self.iconAdd = None
        self.iconFolder = None
        self.iconRename = None
        self.iconConvert = None

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
        save_pixmap = QPixmap(':/toolbar/save_26px.png')
        self.iconSave = QIcon(save_pixmap)
        self.iconSave.addPixmap(save_pixmap, QIcon.Disabled)

        add_pixmap = QPixmap(':/toolbar/add_26px.png')
        self.iconAdd = QIcon(add_pixmap)
        self.iconAdd.addPixmap(add_pixmap, QIcon.Disabled)

        folder_pixmap = QPixmap(':/toolbar/folder_26px.png')
        self.iconFolder = QIcon(folder_pixmap)
        self.iconFolder.addPixmap(folder_pixmap, QIcon.Disabled)

        rename_pixmap = QPixmap(':/toolbar/edit_26px.png')
        self.iconRename = QIcon(rename_pixmap)
        self.iconRename.addPixmap(rename_pixmap, QIcon.Disabled)

        convert_pixmap = QPixmap(':/toolbar/convert_26px.png')
        self.iconConvert = QIcon(convert_pixmap)
        self.iconConvert.addPixmap(convert_pixmap, QIcon.Disabled)
       
        if sys.platform == 'win32':
            self.setIconSize(QSize(32, 32))
        else:
            self.setIconSize(QSize(28, 28))
        self.setIcons()

    def setSmallIcons(self):
        self.iconSave = QIcon(':/toolbar/save_22px.png')
        self.iconAdd = QIcon(':/toolbar/add_22px.png')
        self.iconFolder = QIcon(':/toolbar/folder_22px.png')
        self.iconRename = QIcon(':/toolbar/edit_22px.png')
        self.iconConvert = QIcon(':/toolbar/convert_22px.png')

        if sys.platform == 'win32':
            self.setIconSize(QSize(24, 24))
        else:
            self.setIconSize(QSize(22, 22))
        self.setIcons()

    def setIcons(self):
        for action in self.actions():
            if action.objectName() == 'actionSave_metadata':
                action.setIcon(self.iconSave)
            elif action.objectName() == 'actionAdd_file':
                action.setIcon(self.iconAdd)
            elif action.objectName() == 'actionAdd_folder':
                action.setIcon(self.iconFolder)
            elif action.objectName() == 'actionRename':
                action.setIcon(self.iconRename)
            elif action.objectName() == 'actionConvert':
                action.setIcon(self.iconConvert)
