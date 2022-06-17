import sys
import ctypes
from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon
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
        separator = QWidget(self)
        separator.setFixedWidth(10)
        self.addWidget(separator)

    def setCenterAlign(self):
        spacer1 = QWidget()
        spacer1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        for action in self.actions():
            print(action.objectName())
            self.insertWidget(action, spacer1)
            break
        self.addWidget(spacer2)

    def setLargeIcons(self):
        self.iconSave = QIcon(':/toolbar/save_32px.png')
        self.iconAdd = QIcon(':/toolbar/add_32px.png')
        self.iconFolder = QIcon(':/toolbar/folder_32px.png')
        self.iconRename = QIcon(':/toolbar/edit_32px.png')
        self.iconConvert = QIcon(':/toolbar/convert_32px.png')
       
        self.setIconSize(QSize(36, 36))
        self.setIcons()

    def setSmallIcons(self):
        self.iconSave = QIcon(':/toolbar/save_22px.png')
        self.iconAdd = QIcon(':/toolbar/add_22px.png')
        self.iconFolder = QIcon(':/toolbar/folder_22px.png')
        self.iconRename = QIcon(':/toolbar/edit_22px.png')
        self.iconConvert = QIcon(':/toolbar/convert_22px.png')

        self.setIconSize(QSize(24, 24))
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
