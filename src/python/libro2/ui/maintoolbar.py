import sys
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
import darkdetect


class MainToolbar(QToolBar):
   
    def __init__(self, parent):
        super(MainToolbar, self).__init__(parent)
        self._base_size = 22
        if sys.platform == 'darwin':
            self._is_dark_mode = darkdetect.isDark()
        else:
            self._is_dark_mode = False

        self.setIcons()

    def scale_factor(self):
        if sys.platform == 'darwin':
            base_dpi = 72
        else:
            base_dpi = 96

        return self.screen().logicalDotsPerInchX() / base_dpi

    def setIcons(self):
        size = int(self._base_size * self.scale_factor())
        self.setIconSize(QSize(size, size))
        if self._is_dark_mode:
            icon_add = QIcon(':/toolbar/plus-box_dark.svg')
            icon_add_folder = QIcon(':/toolbar/folder-plus_dark.svg')
            icon_edit = QIcon(':/toolbar/pencil_dark.svg')
            icon_change = QIcon(':/toolbar/swap-horizontal-bold_dark.svg')
            icon_send_file = QIcon(':/toolbar/file-send_dark.svg')
            icon_settings = QIcon(':/toolbar/cog_dark.svg')
        else:
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


    def paintEvent(self, event):
        if sys.platform == 'darwin':
            if self._is_dark_mode != darkdetect.isDark():
                self._is_dark_mode = darkdetect.isDark()
                self.setIcons()
        return super().paintEvent(event)