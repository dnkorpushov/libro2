from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize

from .textviewdialog_ui import Ui_ViewTextDialog


class TextViewDialog(QDialog, Ui_ViewTextDialog):

    def __init__(self, parent, errors, scale_factor=1):
        super(TextViewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Libro2')
        
        base_width = 520 
        base_height = 300 

        self.setMinimumSize(QSize(int(base_width * scale_factor), int(base_height * scale_factor)))  
        self.resize(self.minimumSize())
        self.adjustSize()

        text = ''

        for error in errors:
            if error['src']:
                text += '"{0}"'.format(error['src']) + (' -><br>' if error['dest'] else '<br>')
            if error['dest']:
                text += '"{0}"<br>'.format(error['dest'])
            if error['error']:
                text += '<b><font color="#D0312D">{0}</font></b><br><br>'.format(error['error'])

        self.textEdit.setHtml(text)

 
