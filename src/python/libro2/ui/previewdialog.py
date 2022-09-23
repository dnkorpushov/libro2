from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize, QCoreApplication

from .textviewdialog_ui import Ui_ViewTextDialog
from .smartdialog import SmartDialog

_t = QCoreApplication.translate


class PreviewDialog(SmartDialog, Ui_ViewTextDialog):
    def __init__(self, parent, textarr):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(_t('preview', 'Preview'))
        
        self.restoreSize()

        text = ''

        for line in textarr:
            text += _t('preview', '<b>Source file name: </b>') + ' "{0}"'.format(line['src']) + '<br/>'
            text += _t('preview', '<b>Destination file name:</b>') + ' "{0}"'.format(line['dest']) + '<hr/>'
            
        self.textEdit.setHtml(text)

 
