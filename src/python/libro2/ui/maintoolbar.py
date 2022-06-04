import sys
import ctypes
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize




class MainToolbar(QToolBar):
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
        self.setStyleSheet('QToolBar { border: 0px }')

       
    def setIcons(self):
        
        iconSave = QIcon(':/toolbar/save_30px.png')
        iconAdd = QIcon(':/toolbar/add_file_30px.png')
        iconFolder = QIcon(':/toolbar/add_folder_30px.png')
        iconRename = QIcon(':/toolbar/rename_30px.png')
        iconConvert = QIcon(':/toolbar/convert_30px.png')

        self.setIconSize(QSize(36, 36))

        if sys.platform == 'win32':
            scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            if scaleFactor < 125:
                self.setIconSize(QSize(24, 24))
                iconSave = QIcon(':/toolbar/save_16px.png')
                iconAdd = QIcon(':/toolbar/add_file_16px.png')
                iconFolder = QIcon(':/toolbar/add_folder_16px.png')
                iconRename = QIcon(':/toolbar/rename_16px.png')
                iconConvert = QIcon(':/toolbar/convert_16px.png')

        for action in self.actions():
            if action.objectName() == 'actionSave_metadata':
                action.setIcon(iconSave)
            elif action.objectName() == 'actionAdd_file':
                action.setIcon(iconAdd)
            elif action.objectName() == 'actionAdd_folder':
                action.setIcon(iconFolder)
            elif action.objectName() == 'actionRename':
                action.setIcon(iconRename)
            elif action.objectName() == 'actionConvert':
                action.setIcon(iconConvert)
