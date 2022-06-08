from distutils.log import error
import os
import base64

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint, QByteArray
from PyQt5.QtGui import QIcon

from .mainwindow_ui import Ui_MainWindow
from .addfilesdialog import AddFilesDialog
from .renamedialog import RenameDialog
from .movefilesdialog import MoveFilesDialog
from .textviewdialog import TextViewDialog
from .aboutdialog import AboutDialog
from .convertdialog import ConvertDialog
from .convertfilesdialog import ConvertFilesDialog

import config
import database

settings = config.settings

class MainWindow (QMainWindow, Ui_MainWindow):

    def __init__(self):
        config.load()
        database.init()

        self.prevSplitterSizes = None
        self.isAutoApplyFilter = True

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/icons/course_16px.png'))
        
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
       
        if settings.ui_window_x and settings.ui_window_y:
            self.move(settings.ui_window_x, settings.ui_window_y)

        if settings.ui_window_height and settings.ui_window_width:
            self.resize(settings.ui_window_width, settings.ui_window_height)

        if len(settings.ui_splitter_sizes) > 0:
            if settings.ui_info_panel_visible:
                self.actionViewInfo_panel.setChecked(True)
                self.splitter.setSizes(settings.ui_splitter_sizes)
            else:
                self.actionViewInfo_panel.setChecked(False)
                self.prevSplitterSizes = settings.ui_splitter_sizes
                self.onViewInfoPanel(False)

        
        self.frameFilter.setVisible(settings.ui_filter_panel_visible)
        self.actionFilter_panel.setChecked(settings.ui_filter_panel_visible)
        self.isAutoApplyFilter = settings.ui_auto_apply_filter
        self.textFilter.setMaximumHeight(self.toolFilterButton.maximumHeight())
        self.textFilter.setMinimumHeight(self.toolFilterButton.minimumHeight())
        
        self.textFilter.lineEdit().textChanged.connect(self.setFilterOnTextChanged)
        self.textFilter.lineEdit().returnPressed.connect(self.setFilterOnReturnPressed)

        self.bookInfo.clear()

        self.bookList.setColumnsWidth(settings.ui_columns_width)
        self.bookList.setColumnsOrder(settings.ui_columns_order)
        self.bookList.setHiddenColumns(settings.ui_hidden_columns)
        self.bookList.setHiddenColumnsWidth(settings.ui_hidden_columns_width)
        self.bookList.selectionModel().selectionChanged.connect(self.onBookListSelectionChanged)

        self.toolBar.setIcons()
        self.toolBar.setVisible(settings.ui_toolbar_visible)
        self.actionsSetEnabled(False)
        self.actionSave_metadata.setEnabled(False)
        self.bookInfo.dataChanged.connect(self.OnBookInfoDataChanged)


    def OnBookInfoDataChanged(self, dataChanged):
        self.actionSave_metadata.setEnabled(dataChanged)

    def setFilterOnTextChanged(self):
        if self.isAutoApplyFilter:
            self.setFilter()

    def setFilterOnReturnPressed(self):
        if not self.isAutoApplyFilter:
            self.setFilter()

    def setFilter(self):
        self.bookList.setFilter(self.textFilter.currentText())  

    def onAddFiles(self):
        result = QFileDialog.getOpenFileNames(self, 
                                              caption='Add files', 
                                              directory=settings.add_files_last_selected,
                                              filter='Ebook files (*.fb2 *.fb2.zip *.epub);;All files (*.*)')
        if len(result[0]) > 0:
            self.AddFiles(result[0])
            for file in result[0]:
                (settings.add_files_last_selected, _) = os.path.split(file)

    def onAddFolder(self):
        fileList = []
        folder = QFileDialog.getExistingDirectory(self,
                                                  caption='Add folder',
                                                  directory=settings.add_folder_last_selected)
        if folder:
            settings.add_folder_last_selected = folder
            for root, dir, files in os.walk(folder):
                for file in files:
                    fileList.append(os.path.join(root, file))
        
            self.AddFiles(fileList)

    def AddFiles(self, files):
        loadFilesDialog = AddFilesDialog(self, files)
        loadFilesDialog.exec()
        self.bookList.updateRows()
        errors = loadFilesDialog.getErrors()
        if len(errors) > 0:
            errorDialog = TextViewDialog(self, errors)
            errorDialog.exec()

    def onSelectAll(self):
        self.wait()
        self.bookList.selectAll()
        self.stopWait()

    def onRemoveSelected(self):
        self.wait()
        self.bookList.remove(self.bookList.getSelectedId())
        if self.bookList.model().rowCount() == 0:
            self.bookInfo.clear()
        self.stopWait()

    def wait(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)

    def stopWait(self):
        QApplication.restoreOverrideCursor()

    def getSelectedBookList(self):
        list_id = self.bookList.getSelectedId()
        book_info_list = []
        for id in list_id:
            book_info = database.get_book_info(id)
            book_info_list.append(book_info)
        
        return book_info_list

    def onBookListSelectionChanged(self):
        if self.bookInfo.isDataChanged:
            if QMessageBox.question(self, 'Libro2', 'Save changes?') == QMessageBox.Yes:
                self.SaveMetadata()

        book_info_list = self.getSelectedBookList()

        if len(book_info_list) > 0:
            self.actionsSetEnabled(True)
            self.bookInfo.setData(book_info_list)
        else:
            self.bookInfo.clear()
            self.actionsSetEnabled(False)

    def actionsSetEnabled(self, enabled):
        self.actionRename.setEnabled(enabled)
        self.actionConvert.setEnabled(enabled)


    def onViewFilterPanel(self, isVisible):
        self.frameFilter.setVisible(isVisible)
        if not isVisible:
            self.bookList.setFilter('')
        else:
            self.setFilter()
            self.textFilter.setFocus(True)
    
    def onViewInfoPanel(self, checked):
        self.splitter.setChildrenCollapsible(not checked)

        if checked:
            self.splitter.setHandleWidth(3)
            self.splitter.setSizes(self.prevSplitterSizes)
        else:
            self.prevSplitterSizes = self.splitter.sizes()
            self.splitter.setHandleWidth(0)
            self.splitter.setSizes((0, 1))

    def onViewToolbar(self, checked):
        self.toolBar.setVisible(checked)
    
    def onSaveMetadata(self):
        if self.bookInfo.isDataChanged:
            self.SaveMetadata()

    def SaveMetadata(self):
        self.wait()
        book_info_list = self.bookInfo.getData()
        errors = []
        for book_info in book_info_list:
            try:
                database.update_book_info(book_info)
            except Exception as e:
                errors.append({ 'src': book_info.file, 'dest': None, 'error': str(e) })
        self.bookInfo.isDataChanged = False
        self.actionSave_metadata.setEnabled(False)
        
        self.bookList.updateRows()
        self.stopWait()

        if len(errors) > 0:
            errorDialog = TextViewDialog(self, errors)
            errorDialog.exec()
     
    def onRename(self):
        book_info_list = self.getSelectedBookList()
        if len(book_info_list):
            renameDialog = RenameDialog(self)
            renameDialog.bookList = book_info_list
            renameDialog.authorFormat = settings.rename_author_format
            renameDialog.filenameFormat = settings.rename_filename_format
            renameDialog.overwriteExistingFiles = settings.rename_overwrite
            renameDialog.backupBeforeRename = settings.rename_backup

            if renameDialog.exec_():
                self.wait()
                moveFilesDialog = MoveFilesDialog(self, 
                                                  book_info_list, 
                                                  renameDialog.filenameFormat, 
                                                  renameDialog.authorFormat,
                                                  renameDialog.backupBeforeRename,
                                                  renameDialog.overwriteExistingFiles)
                moveFilesDialog.exec()
                self.bookList.updateRows()
                self.stopWait()
                        
                settings.rename_author_format = renameDialog.authorFormat
                settings.rename_filename_format = renameDialog.filenameFormat
                settings.rename_overwrite = renameDialog.overwriteExistingFiles
                settings.rename_backup = renameDialog.backupBeforeRename

                errors = moveFilesDialog.getErrors()
                if len(errors) > 0:
                    errorDialog = TextViewDialog(self, errors)
                    errorDialog.exec()
            
    def onConvert(self):
        convertDialog = ConvertDialog(self)
        convertDialog.outputFormat = settings.convert_output_format
        convertDialog.outputPath = settings.convert_output_path
        convertDialog.overwrite = settings.convert_overwrite
        convertDialog.converterPath = settings.convert_converter_path
        convertDialog.converterConfig = settings.convert_converter_config

        if convertDialog.exec_():
            book_info_list = self.getSelectedBookList()
            convertProgress = ConvertFilesDialog(self, 
                                                 book_info_list=book_info_list,
                                                 out_format=convertDialog.outputFormat,
                                                 out_path=convertDialog.outputPath,
                                                 overwrite=convertDialog.overwrite,
                                                 converter_path=convertDialog.converterPath,
                                                 converter_config=convertDialog.converterConfig)
            convertProgress.exec()

            if len(convertProgress.errors) > 0:
                errorDialog = TextViewDialog(self, convertProgress.errors)
                errorDialog.exec()
            
            settings.convert_output_format = convertDialog.outputFormat
            settings.convert_output_path = convertDialog.outputPath
            settings.convert_overwrite = convertDialog.overwrite 
            settings.convert_converter_path = convertDialog.converterPath
            settings.convert_converter_config = convertDialog.converterConfig

    def onToolFilterButton(self):
        actionList = {
            'title': 'Title',
            'author': 'Author',
            'series': 'Series',
            'tags': 'Tags',
            'lang': 'Lang',
            'translator': 'Translator',
            'type': 'Type',
            'file': 'File' 
        }
        menu = QMenu()
        for key in actionList:
            acitonItem = menu.addAction(actionList[key])
            acitonItem.setData(key)

        menu.addSeparator()

        actionItem = menu.addAction('AND')
        actionItem.setData('AND')
        actionItem = menu.addAction('OR')
        actionItem.setData('OR')

        menu.addSeparator()
        actionItem = QAction('Auto-apply filter', parent=menu, checkable=True, checked=self.isAutoApplyFilter)
        actionItem.setData('AutoApplyFilter')
        menu.addAction(actionItem)
        
        menu_x = -1 * menu.sizeHint().width() + self.toolFilterButton.width()
        menu_y = -1 * menu.sizeHint().height() + self.toolFilterButton.height()
        
        action = menu.exec_(self.toolFilterButton.mapToGlobal(QPoint(menu_x , menu_y)))
        if action:
            if action.data() == 'AutoApplyFilter':
                self.isAutoApplyFilter = not self.isAutoApplyFilter
            elif action.data() in ('AND', 'OR'):
                self.textFilter.setCurrentText(self.textFilter.currentText() + ' {} '.format(action.data()))
            else:
                self.textFilter.setCurrentText(self.textFilter.currentText() + ' {}:'.format(action.data()))
            self.textFilter.setFocus(True)


    def onAbout(self):
        about = AboutDialog(self)
        about.exec()

    def onAboutQt(self):
        QMessageBox.aboutQt(self)

    def closeEvent(self, e):
        self.exitApp()

    def onExit(self):
        self.close()

    def exitApp(self):
        settings.ui_window_x = self.pos().x()
        settings.ui_window_y = self.pos().y()
        settings.ui_window_width = self.size().width()
        settings.ui_window_height = self.size().height()
        settings.ui_info_panel_visible = self.actionViewInfo_panel.isChecked()
        settings.ui_filter_panel_visible = self.actionFilter_panel.isChecked()
        settings.ui_toolbar_visible = self.toolBar.isVisible()
        settings.ui_auto_apply_filter = self.isAutoApplyFilter
        settings.ui_columns_order = self.bookList.getColumnsOrder()
        settings.ui_columns_width = self.bookList.getColumnsWidth()
        settings.ui_hidden_columns = self.bookList.getHiddenColumns()
        settings.ui_hidden_columns_width = self.bookList.getHiddenColumnsWidth()

        if self.actionViewInfo_panel.isChecked():
            settings.ui_splitter_sizes = self.splitter.sizes()
        else:
            settings.ui_splitter_sizes = self.prevSplitterSizes;

        config.save()
        database.clear()




