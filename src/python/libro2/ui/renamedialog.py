import os
import sys
import subprocess
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

        self._author_format_list = set()
        self._filename_format_list = set()

        self.textAuthorFormat.clicked.connect(self.onTextAuthorFormatClick)
        self.textAuthorFormat.textChanged.connect(self.generateSample)

        self.textFilenameFormat.clicked.connect(self.onTextFilenameFormatClick)
        self.textFilenameFormat.textChanged.connect(self.generateSample)

        self.checkDeleteSource.stateChanged.connect(self.onDeleteSourceClick)
        self.radioRenameInSourceFolder.clicked.connect(self.setRenameDestination)
        self.radioRenameMoveTo.clicked.connect(self.setRenameDestination)

    @property
    def authorFormat(self):
        return self.textAuthorFormat.text()

    @property
    def filenameFormat(self):
        return self.textFilenameFormat.text()

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
        return list(self._author_format_list)

    @property 
    def filenameFormatList(self):
        return list(self._filename_format_list)

    @property
    def renameInSourceFolder(self):
        return self.radioRenameInSourceFolder.isChecked()

    @property
    def renameMoveToFolder(self):
        return self.textMoveToFolder.text()
    
    @authorFormatList.setter
    def authorFormatList(self, values):
        if values:
            for val in values:
                self._author_format_list.add(val)

    @filenameFormatList.setter
    def filenameFormatList(self, values):
        if values:
            for val in values:
                self._filename_format_list.add(val)

    @deleteSourceFiles.setter
    def deleteSourceFiles(self, value):
        self.checkDeleteSource.setChecked(value)
        self.onDeleteSourceClick()

    @authorFormat.setter
    def authorFormat(self, value):
        self.textAuthorFormat.setText(value)

    @filenameFormat.setter
    def filenameFormat(self, value):
        self.textFilenameFormat.setText(value)

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

    @renameInSourceFolder.setter
    def renameInSourceFolder(self, value):
        self.radioRenameInSourceFolder.setChecked(value)
        self.radioRenameMoveTo.setChecked(not value)
        self.textMoveToFolder.setEnabled(not value)
        
    @renameMoveToFolder.setter
    def renameMoveToFolder(self, value):
        self.textMoveToFolder.setText(value)

    def setRenameDestination(self):
        self.renameInSourceFolder = self.radioRenameInSourceFolder.isChecked()

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
        dest_path = ''
        out_file = os.path.join(config.config_path, 'preview.txt')
        for book in self.bookList:
            meta = ebookmeta.get_metadata(book.file)
            new_filename = meta.get_filename_by_pattern(self.filenameFormat, self.authorFormat, 2)
            if self.renameInSourceFolder:
                dest_path = os.path.dirname(meta.file)
            else:
                dest_path = self.renameMoveToFolder
            new_file = os.path.normpath(os.path.join(dest_path, new_filename))
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


    def onTextAuthorFormatClick(self):
        elements = {
            _t('ren', 'First name'): '#f',
            _t('ren', 'Middle name'): '#m',
            _t('ren', 'Last name'): '#l',
            _t('ren', 'Fist name initial'): '#fi',
            _t('ren', 'Middle name initial'): '#mi'
        }
        self.toolContextMenu(elements=elements, 
                             templateSet=self._author_format_list,
                             control=self.textAuthorFormat, 
                             point=self.textAuthorFormat.mapToGlobal(QPoint(self.textAuthorFormat.width(), 0)))

    def onTextFilenameFormatClick(self):
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
        self.toolContextMenu(elements=elements, 
                             templateSet=self._filename_format_list,
                             control=self.textFilenameFormat, 
                             point=self.textFilenameFormat.mapToGlobal(QPoint(self.textFilenameFormat.width(), 0)))
       
    def toolContextMenu(self, elements, templateSet, control, point):
        menu = QMenu()
        for key in elements:
            item = menu.addAction(key)
            item.setData(('template_element', elements[key]))
        
        templateList = list(templateSet)
        if len(templateList) > 0:
            menu.addSeparator()
            templateMenu = QMenu(_t('ren', 'Saved templates'))
            for template in templateList:
                item = templateMenu.addAction(template)
                item.setData(('saved_template', template))
            menu.addMenu(templateMenu)

        menu.addSeparator()
        item = menu.addAction(_t('ren', 'Save current template to list'))
        item.setData(('save_action', ''))
        item = menu.addAction(_t('ren', 'Delete current template from list'))
        item.setData(('delete_action', ''))
        action = menu.exec_(point)
        if action:
            element = action.data()
            text = control.text()
            
            if element[0] == 'save_action':
                templateSet.add(text)

            elif element[0] == 'delete_action':
                templateSet.discard(text)
            
            elif element[0] == 'saved_template':
                control.setText(element[1])
            
            elif element[0] == 'template_element':
                if control.lineEdit().selectionStart() == -1:
                    pos = control.lineEdit().cursorPosition()
                    text = text[:pos] + element[1] + text[pos:]
                    control.setText(text)
                    control.lineEdit().setCursorPosition(pos + len(element[1]))
                else:
                    start = control.lineEdit().selectionStart()
                    end = control.lineEdit().selectionEnd()
                    text = text[:start] + element[1] + text[end:]
                    control.setText(text)
                    control.lineEdit().setCursorPosition(start + len(element[1]))

