import os
import webbrowser
import ebookmeta
import traceback

from PyQt5.QtWidgets import QDialog, QMenu, QApplication, QFileDialog
from PyQt5.QtCore import QPoint, Qt, QCoreApplication, QSize
from .renamedialog_ui import Ui_RenameDialog
from .previewdialog import PreviewDialog
from .smartdialog import SmartDialog

import format_filename

_t = QCoreApplication.translate

HELP_URL = 'https://github.com/dnkorpushov/libro2/wiki/%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%D1%8B'

class RenameDialog(Ui_RenameDialog, SmartDialog):
    def __init__(self, parent):
        super(RenameDialog, self).__init__(parent)
        self.setupUi(self)

        self.restoreSize()

        self._book_list = []

        self._author_format_list = set()
        self._translator_format_list = set()
        self._filename_format_list = set()
        self._path_list = set()

        self.textMoveToFolder.clicked.connect(self.onTextMoveToFolderClick)

        self.textAuthorFormat.clicked.connect(self.onTextAuthorFormatClick)
        self.textAuthorFormat.textChanged.connect(self.generateSample)

        self.textTranslatorFormat.clicked.connect(self.onTextTranslatorFormatClick)
        self.textTranslatorFormat.textChanged.connect(self.generateSample)

        self.textFilenameFormat.clicked.connect(self.onTextFilenameFormatClick)
        self.textFilenameFormat.textChanged.connect(self.generateSample)

        self.checkDeleteSource.stateChanged.connect(self.onDeleteSourceClick)
        self.radioRenameInSourceFolder.clicked.connect(self.setRenameDestination)
        self.radioRenameMoveTo.clicked.connect(self.setRenameDestination)

        self.buttonHelp.clicked.connect(self.onHelpButtonClick)

    @property
    def authorFormat(self):
        return self.textAuthorFormat.text()

    @property
    def translatorFormat(self):
        return self.textTranslatorFormat.text()

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
    def translatorFormatList(self):
        return list(self._translator_format_list)

    @property 
    def filenameFormatList(self):
        return list(self._filename_format_list)

    @property
    def renamePathList(self):
        return list(self._path_list)

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

    @translatorFormatList.setter
    def translatorFormatList(self, values):
        if values:
            for val in values:
                self._translator_format_list.add(val)

    @filenameFormatList.setter
    def filenameFormatList(self, values):
        if values:
            for val in values:
                self._filename_format_list.add(val)

    @renamePathList.setter
    def renamePathList(self, values):
        if values:
            for val in values:
                self._path_list.add(val)
                
    @deleteSourceFiles.setter
    def deleteSourceFiles(self, value):
        self.checkDeleteSource.setChecked(value)
        self.onDeleteSourceClick()

    @authorFormat.setter
    def authorFormat(self, value):
        self.textAuthorFormat.setText(value)

    @translatorFormat.setter
    def translatorFormat(self, value):
        self.textTranslatorFormat.setText(value)

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
            try:
                self.labelSample.setText(format_filename.filename_by_template(meta, self.filenameFormat, self.authorFormat, self.translatorFormat))
            except Exception as e:
                self.labelSample.setText(_t('ren', 'Format error'))
            break

    def onPreviewClick(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out_str = ''
        dest_path = ''
        preview_output = []
        for book in self.bookList:
            meta = ebookmeta.get_metadata(book.file)
            try:
                new_filename = format_filename.filename_by_template(meta, self.filenameFormat, self.authorFormat, self.translatorFormat)
                if self.renameInSourceFolder:
                    dest_path = os.path.dirname(meta.file)
                else:
                    dest_path = self.renameMoveToFolder
                new_file = os.path.normpath(os.path.join(dest_path, new_filename))
            except:
                new_file = _t('ren', 'Format error:' + traceback.format_exc())
            preview_output.append({'src': book.file, 'dest': new_file})
        QApplication.restoreOverrideCursor()

        previewDialog = PreviewDialog(self, preview_output)
        previewDialog.exec()

    def onTextAuthorFormatClick(self):
        elements = {
            _t('ren', 'First name'): '{firstname}',
            _t('ren', 'Middle name'): '{middlename}',
            _t('ren', 'Last name'): '{lastname}',
            _t('ren', 'Fist name initial'): '{f}',
            _t('ren', 'Middle name initial'): '{m}'
        }

        base_templates = {
            _t('ren', 'Firstname Lastname'): '{firstname} {lastname}',
            _t('ren', 'Lastname Firtsname'): '{lastname} {firstname}',
            _t('ren', 'Lastname F'): '{lastname} {f}',
            _t('ren', 'Lastname F. M'): '{lastname} {f}{iif(m, ". " + m)}'
        }

        self.toolContextMenu(elements=elements, 
                             base_templates=base_templates,
                             templateSet=self._author_format_list,
                             control=self.textAuthorFormat, 
                             point=self.textAuthorFormat.mapToGlobal(QPoint(self.textAuthorFormat.width(), 0)))


    def onTextTranslatorFormatClick(self):
        elements = {
            _t('ren', 'First name'): '{firstname}',
            _t('ren', 'Middle name'): '{middlename}',
            _t('ren', 'Last name'): '{lastname}',
            _t('ren', 'Fist name initial'): '{f}',
            _t('ren', 'Middle name initial'): '{m}'
        }

        base_templates = {
            _t('ren', 'Firstname Lastname'): '{firstname} {lastname}',
            _t('ren', 'Lastname Firtsname'): '{lastname} {firstname}',
            _t('ren', 'Lastname F'): '{lastname} {f}',
            _t('ren', 'Lastname F. M'): '{lastname} {f}{iif(m, ". " + m)}'
        }

        self.toolContextMenu(elements=elements, 
                             base_templates=base_templates,
                             templateSet=self._translator_format_list,
                             control=self.textTranslatorFormat, 
                             point=self.textTranslatorFormat.mapToGlobal(QPoint(self.textTranslatorFormat.width(), 0)))

    def onTextFilenameFormatClick(self):
        elements = {
            'title': '{title}',
            'series': '{series}',
            'abbrseries': '{abbrseries}',
            'seriesindex': '{seriesindex}',
            'author': '{author}',
            'authors': '{lst(authors)}',
            'translator': '{translator}',
            'translators': '{lst(translators)}',
            'bookid': '{bookid}',
            'md5':  '{md5}'
        }
        
        base_templates = {
            _t('ren', 'Author. Title'): '{author}. {title}',
            _t('ren', 'Author. Title (tr. Translator)'): '{author}. {title}{iif(translator, " (пер. " + translator + ")")}',
            _t('ren', 'Author. (Series Index) Title'): '{author}. {iif(series, "("+series)}{iif(seriesindex, " " + seriesindex.zfill(2))}{iif(series, ") ")}{title}',
            _t('ren', 'Author/Author. Title (tr. Translator)'): '{path(author)}{author}. {title}{iif(translator, " (пер. " + translator + ")")}',
            _t('ren', 'Author/Author. (Series Index) Title'): '{path(author)}{author}. {iif(series, "("+series)}{iif(seriesindex, " " + seriesindex.zfill(2))}{iif(series, ") ")}{title}',
            _t('ren', 'Author/Series/Index. Title'): '{path(author, series)}{iif(seriesindex, seriesindex.zfill(2) + ". ")}{title}'
        }
        
        self.toolContextMenu(elements=elements, 
                             base_templates=base_templates,
                             templateSet=self._filename_format_list,
                             control=self.textFilenameFormat, 
                             point=self.textFilenameFormat.mapToGlobal(QPoint(self.textFilenameFormat.width(), 0)))

    def onTextMoveToFolderClick(self):
        menu = QMenu()
        item = menu.addAction(_t('ren', 'Browse...'))
        item.setData(('browse_action', ''))
        if len(self._path_list) > 0:
            menu.addSeparator()
            pathListMenu = QMenu(_t('ren', 'Saved path list'))
            for p in self._path_list:
                item = pathListMenu.addAction(p)
                item.setData(('saved_path', p))
            menu.addMenu(pathListMenu)
        menu.addSeparator()
        item = menu.addAction(_t('ren', 'Save current path in list'))
        item.setData(('save_action', ''))
        item = menu.addAction(_t('ren', 'Delete current path from list'))
        item.setData(('delete_action', ''))
        
        action = menu.exec_(self.textMoveToFolder.mapToGlobal(QPoint(self.textMoveToFolder.width(), 0)))
        if action:
            element = action.data()

            if element[0] == 'browse_action':
                result = QFileDialog.getExistingDirectory(directory=self.textMoveToFolder.text())
                if result:
                    self.textMoveToFolder.setText(os.path.normpath(result))
            elif element[0] == 'saved_path':
                self.textMoveToFolder.setText(element[1])
            elif element[0] == 'save_action':
                if self.textMoveToFolder.text():
                    self._path_list.add(os.path.normpath(self.textMoveToFolder.text()))
            elif element[0] == 'delete_action':              
                    self._path_list.discard(os.path.normpath(self.textMoveToFolder.text()))
       
    def toolContextMenu(self, elements, base_templates, templateSet, control, point):
        menu = QMenu()
        for key in elements:
            item = menu.addAction(key)
            item.setData(('template_element', elements[key]))

        menu.addSeparator()
        baseTemplateMenu = QMenu(_t('ren', 'Base templates'))
        for key in base_templates:
            item = baseTemplateMenu.addAction(key)
            item.setData(('base_template', base_templates[key]))
        menu.addMenu(baseTemplateMenu)
            
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
            
            elif element[0] in ('saved_template', 'base_template'):
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


    def onHelpButtonClick(self):
        browser = webbrowser.get()
        browser.open_new_tab(HELP_URL)