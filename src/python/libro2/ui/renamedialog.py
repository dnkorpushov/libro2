import os
import sys
import subprocess
import ebookmeta
import codecs

from PyQt5.QtWidgets import QDialog, QMenu, QApplication
from PyQt5.QtCore import QPoint, Qt
from .renamedialog_ui import Ui_RenameDialog
import config



class RenameDialog(Ui_RenameDialog, QDialog):
    def __init__(self, parent):
        super(RenameDialog, self).__init__(parent)
        self.setupUi(self)
        self._book_list = []

        self.textAuthorFormat.lineEdit().textChanged.connect(self.generateSample)
        self.textFilenameFormat.lineEdit().textChanged.connect(self.generateSample)
        self.toolFilename.clicked.connect(self.onToolFilenameClick)
        self.toolAuthor.clicked.connect(self.onToolAuthorClick)
        self.checkDeleteSource.stateChanged.connect(self.onDeleteSourceClick)

    @property
    def authorFormat(self):
        return self.textAuthorFormat.currentText()

    @property
    def filenameFormat(self):
        return self.textFilenameFormat.currentText()

    @property
    def bookList(self):
        return self._book_list

    @property
    def backupBeforeRename(self):
        return self.checkBackup.isChecked()

    @property
    def overwriteExistingFiles(self):
        return self.checkOverwrite.isChecked()

    @property
    def deleteSourceFiles(self):
        return self.checkDeleteSource.isChecked()

    @deleteSourceFiles.setter
    def deleteSourceFiles(self, value):
        self.checkDeleteSource.setChecked(value)
        self.onDeleteSourceClick()

    @authorFormat.setter
    def authorFormat(self, value):
        self.textAuthorFormat.setCurrentText(value)

    @filenameFormat.setter
    def filenameFormat(self, value):
        self.textFilenameFormat.setCurrentText(value)

    @bookList.setter
    def bookList(self, value):
        self.generateSample()
        self._book_list = value

    @backupBeforeRename.setter
    def backupBeforeRename(self, value):
        self.checkBackup.setChecked(value)
    
    @overwriteExistingFiles.setter
    def overwriteExistingFiles(self, value):
        self.checkOverwrite.setChecked(value)

    def onDeleteSourceClick(self):
        if self.checkDeleteSource.isChecked():
            self.checkBackup.setEnabled(True)
        else: 
            self.checkBackup.setEnabled(False)

    def generateSample(self):
        for book in self._book_list:
            meta = ebookmeta.get_metadata(book.file)
            self.labelSample.setText(ebookmeta.get_filename_from_pattern(meta, self.filenameFormat, self.authorFormat, 2))
            break

    def onPreviewClick(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_str = ''
        out_file = os.path.join(config.config_path, 'preview.txt')
        for book in self.bookList:
            meta = ebookmeta.get_metadata(book.file)
            new_filename = ebookmeta.get_filename_from_pattern(meta, self.filenameFormat, self.authorFormat, 2)
            new_file = os.path.normpath(os.path.join(os.path.dirname(meta.file), new_filename))
            out_str +=  '"{0}" ->\n"{1}"\n\n'.format(os.path.normpath(meta.file), new_file)
        QApplication.restoreOverrideCursor()

        with codecs.open(out_file, 'w') as f:
            f.write(out_str)

            if sys.platform == 'win32':
                os.startfile(out_file)
            elif sys.platform == 'darwin':
                subprocess.call(('open', out_file))
            else:
                subprocess.call(('xdg-open', out_file))


    def onToolAuthorClick(self):
        elements = {
            'First name': '#f',
            'Middle name': '#m',
            'Last name': '#l',
            'Fist name initial': '#fi',
            'Middle name initial': '#mi'
      
        }
        self.toolContextMenu(elements, self.textAuthorFormat, self.toolAuthor.mapToGlobal(QPoint(0, 0)))

    def onToolFilenameClick(self):
        elements = {
            'title': '#title',
            'series': '#series',
            'abbrseries': '#abbrseries',
            'ABBRseries': '#ABBRseries',
            'number': '#number',
            'padnumber(2)': '#padnumber',
            'author': '#author',
            'authors': '#authors',
            'translator': '#translator',
            'bookid': '#bookid'
        }
        self.toolContextMenu(elements, self.textFilenameFormat, self.toolFilename.mapToGlobal(QPoint(0, 0)))
       
    def toolContextMenu(self, elements, control, point):
        menu = QMenu()
        for key in elements:
            item = menu.addAction(key)
            item.setData(elements[key])
        
        action = menu.exec_(point)
        if action:
            element = action.data()
            text = control.currentText()
            if control.lineEdit().selectionStart() == -1:
                pos = control.lineEdit().cursorPosition()
                text = text[:pos] + element + text[pos:]
                control.setCurrentText(text)
                control.lineEdit().setCursorPosition(pos + len(element))
            else:
                start = control.lineEdit().selectionStart()
                end = control.lineEdit().selectionEnd()
                text = text[:start] + element + text[end:]
                control.setCurrentText(text)
                control.lineEdit().setCursorPosition(start + len(element))

