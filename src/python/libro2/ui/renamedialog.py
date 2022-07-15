import os
import sys
import subprocess
from tkinter.ttk import Separator
import ebookmeta
import codecs

from PyQt5.QtWidgets import QDialog, QMenu, QApplication, QLineEdit
from PyQt5.QtCore import QPoint, Qt, QCoreApplication
from PyQt5.QtGui import QIcon
from .renamedialog_ui import Ui_RenameDialog
import config

_t = QCoreApplication.translate

class RenameDialog(Ui_RenameDialog, QDialog):
    def __init__(self, parent):
        super(RenameDialog, self).__init__(parent)
        self.setupUi(self)
        self._book_list = []

        self.customAuthorFormatLineEdit = QLineEdit()
        action = self.customAuthorFormatLineEdit.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolAuthorClick)
        self.textAuthorFormat.setLineEdit(self.customAuthorFormatLineEdit)

        self.customFilenameFormatLineEdit = QLineEdit()
        action = self.customFilenameFormatLineEdit.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolFilenameClick)
        self.textFilenameFormat.setLineEdit(self.customFilenameFormatLineEdit)

        self.textAuthorFormat.lineEdit().textChanged.connect(self.generateSample)
        self.textFilenameFormat.lineEdit().textChanged.connect(self.generateSample)
        
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

    @property
    def authorFormatList(self):
        return [self.textAuthorFormat.itemText(i) for i in range(self.textAuthorFormat.count())]

    @property 
    def filenameFormatList(self):
        return [self.textFilenameFormat.itemText(i) for i in range(self.textFilenameFormat.count())]

    @authorFormatList.setter
    def authorFormatList(self, values):
        for val in values:
            self.textAuthorFormat.addItem(val)

    @filenameFormatList.setter
    def filenameFormatList(self, values):
        for val in values:
            self.textFilenameFormat.addItem(val)

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
            self.labelSample.setText(meta.get_filename_by_pattern(self.filenameFormat, self.authorFormat, 2))
            break

    def onPreviewClick(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_str = ''
        out_file = os.path.join(config.config_path, 'preview.txt')
        for book in self.bookList:
            meta = ebookmeta.get_metadata(book.file)
            new_filename = meta.get_filename_by_pattern(self.filenameFormat, self.authorFormat, 2)
            new_file = os.path.normpath(os.path.join(os.path.dirname(meta.file), new_filename))
            out_str +=  '"{0}" ->\n"{1}"\n\n'.format(os.path.normpath(meta.file), new_file)
        QApplication.restoreOverrideCursor()

        with codecs.open(out_file, 'w') as f:
            f.write(out_str)
            f.close()

            if sys.platform == 'win32':
                os.startfile(out_file)
            elif sys.platform == 'darwin':
                subprocess.call(('open', out_file))
            else:
                subprocess.call(('xdg-open', out_file))


    def onToolAuthorClick(self):
        elements = {
            _t('ren', 'First name'): '#f',
            _t('ren', 'Middle name'): '#m',
            _t('ren', 'Last name'): '#l',
            _t('ren', 'Fist name initial'): '#fi',
            _t('ren', 'Middle name initial'): '#mi'
        }
        self.toolContextMenu(elements, self.textAuthorFormat, 
                             self.customAuthorFormatLineEdit.mapToGlobal(QPoint(self.customAuthorFormatLineEdit.width(), 0)))

    def onToolFilenameClick(self):
        elements = {
            'Title': '#Title',
            'Series': '#Series',
            'Abbrseries': '#Abbrseries',
            'Number': '#Number',
            'Padnumber(2)': '#Padnumber',
            'Author': '#Author',
            'Authors': '#Authors',
            'Translator': '#Translator',
            'Atranslator': '#Atranslator',
            'Atranslators': '#Atranslators',
            'Bookid': '#Bookid',
            'Md5':  '#Md5'
        }
        self.toolContextMenu(elements, self.textFilenameFormat, 
                             self.customFilenameFormatLineEdit.mapToGlobal(QPoint(self.customFilenameFormatLineEdit.width(), 0)))
       
    def toolContextMenu(self, elements, control, point):
        menu = QMenu()
        for key in elements:
            item = menu.addAction(key)
            item.setData(elements[key])
        
        menu.addSeparator()
        item = menu.addAction(_t('ren', 'Save current template to list'))
        item.setData('__save__')
        item = menu.addAction(_t('ren', 'Delete current template from list'))
        item.setData('__delete__')
        action = menu.exec_(point)
        if action:
            element = action.data()
            text = control.currentText()
            if element == '__save__':
                if control.findText(text) == -1:
                    control.addItem(text)

            elif element == '__delete__':
                index = control.findText(text)
                if index > -1:
                    control.removeItem(index)
            else:
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

