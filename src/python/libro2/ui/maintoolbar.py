from PyQt5.QtWidgets import QToolBar
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize


class MainToolbar(QToolBar):
   
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
        self._base_size = 22

    def setIconScale(self, scale):
        size = int(self._base_size * scale)
        self.setIconSize(QSize(size, size))
        icon_add = QIcon(':/toolbar/plus-box.svg')
        icon_add_folder = QIcon(':/toolbar/folder-plus.svg')
        icon_edit = QIcon(':/toolbar/pencil.svg')
        icon_change = QIcon(':/toolbar/swap-horizontal-bold.svg')
        icon_send_file = QIcon(':/toolbar/file-send.svg')
        icon_settings = QIcon(':/toolbar/cog.svg')
        
        for action in self.actions():
            if action.objectName() == 'actionAdd_file':
                action.setIcon(QIcon(icon_add))
            elif action.objectName() == 'actionAdd_folder':
                action.setIcon(QIcon(icon_add_folder))
            elif action.objectName() == 'actionEdit_metadata':
                action.setIcon(QIcon(icon_edit))
            elif action.objectName() == 'actionRename':
                action.setIcon(QIcon(icon_change))
            elif action.objectName() == 'actionConvert':
                action.setIcon(QIcon(icon_send_file))
            elif action.objectName() == 'actionSettings':
                action.setIcon(QIcon(icon_settings))

