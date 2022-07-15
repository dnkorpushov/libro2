from PyQt5.QtWidgets import QDialog

from .textviewdialog_ui import Ui_ViewTextDialog


class TextViewDialog(QDialog, Ui_ViewTextDialog):

    def __init__(self, parent, errors):
        super(TextViewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Libro2')
        
        text = ''

        for error in errors:
            if error['src']:
                text += '"{0}"'.format(error['src']) + (' -><br>' if error['dest'] else '<br>')
            if error['dest']:
                text += '"{0}"<br>'.format(error['dest'])
            if error['error']:
                text += '<b><font color="#D0312D">{0}</font></b><br><br>'.format(error['error'])

        self.textEdit.setHtml(text)

 
