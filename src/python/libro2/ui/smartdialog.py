import sys
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize

import config

settings = config.settings

class SmartDialog(QDialog):
    def __init__(self, parent):
        super(SmartDialog, self).__init__(parent)

    def restoreSize(self):
        base_width = int(self.geometry().width() * self.scale_factor())
        base_height = int(self.geometry().height() * self.scale_factor())

        self.setMinimumSize(QSize(base_width, base_height))

        if self.__class__.__name__ in settings.ui_dialog_size.keys():
            (width, height) = settings.ui_dialog_size[self.__class__.__name__]
            self.resize(QSize(width, height))
        else:
            self.resize(self.minimumSize())

    def closeEvent(self, event):
        self._save_size()
        return super().closeEvent(event)

    def accept(self):
        self._save_size()
        return super().accept()
    
    def reject(self):
        self._save_size()
        return super().reject()

    def scale_factor(self):
        if sys.platform == 'darwin':
            base_dpi = 72
        else:
            base_dpi = 96

        return self.screen().logicalDotsPerInchX() / base_dpi

    def _save_size(self):
        if self.size().width() == self.minimumSize().width() and self.size().height() == self.minimumSize().height():
            if self.__class__.__name__ in settings.ui_dialog_size.keys():
                del settings.ui_dialog_size[self.__class__.__name__]
        else:
            settings.ui_dialog_size[self.__class__.__name__] = (self.width(), self.height())
