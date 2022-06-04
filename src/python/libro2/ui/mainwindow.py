import os

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon

from .mainwindow_ui import Ui_MainWindow
from .addfilesdialog import AddFilesDialog
from .renamedialog import RenameDialog

import config
import database


class MainWindow (QMainWindow, Ui_MainWindow):

    def __init__(self):
        config.load()
        database.init()

        self.prevSplitterSizes = None
        self.isAutoApplyFilter = True

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/icons/books.ico'))
        
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
       
        if config.ui_window_x and config.ui_window_y:
            self.move(config.ui_window_x, config.ui_window_y)

        if config.ui_window_height and config.ui_window_width:
            self.resize(config.ui_window_width, config.ui_window_height)

        if len(config.ui_splitter_sizes) > 0:
            if config.ui_info_panel_visible:
                self.actionViewInfo_panel.setChecked(True)
                self.splitter.setSizes(config.ui_splitter_sizes)
            else:
                self.actionViewInfo_panel.setChecked(False)
                self.prevSplitterSizes = config.ui_splitter_sizes
                self.onViewInfoPanel(False)

        self.frameFilter.setVisible(config.ui_filter_panel_visible)
        self.actionFilter_panel.setChecked(config.ui_filter_panel_visible)
        self.isAutoApplyFilter = config.ui_auto_apply_filter
        self.textFilter.setMaximumHeight(self.toolFilterButton.maximumHeight())
        self.textFilter.setMinimumHeight(self.toolFilterButton.minimumHeight())
        
        self.textFilter.lineEdit().textChanged.connect(self.setFilterOnTextChanged)
        self.textFilter.lineEdit().returnPressed.connect(self.setFilterOnReturnPressed)

        self.bookInfo.clear()

        self.bookList.selectionModel().selectionChanged.connect(self.onBookListSelectionChanged)

        self.toolBar.setIcons()
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
                                              directory=config.add_files_last_selected,
                                              filter='Ebook files (*.fb2 *.fb2.zip *.epub);;All files (*.*)')
        if len(result[0]) > 0:
            self.AddFiles(result[0])
            for file in result[0]:
                (config.add_files_last_selected, _) = os.path.split(file)

    def onAddFolder(self):
        fileList = []
        folder = QFileDialog.getExistingDirectory(self,
                                                  caption='Add folder',
                                                  directory=config.add_folder_last_selected)
        if folder:
            config.add_folder_last_selected = folder
            for root, dir, files in os.walk(folder):
                for file in files:
                    fileList.append(os.path.join(root, file))
        
            self.AddFiles(fileList)

    def AddFiles(self, files):
        loadFilesDialog = AddFilesDialog(self, files)
        loadFilesDialog.exec()
        self.bookList.updateRows()

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

    def onBookListSelectionChanged(self):
        if self.bookInfo.isDataChanged:
            if QMessageBox.question(self, 'Libro2', 'Save changes?') == QMessageBox.Yes:
                self.SaveMetadata()

        list_id = self.bookList.getSelectedId()
        book_info_list = []

        if len(list_id) > 0:
            self.actionsSetEnabled(True)
            for id in list_id:
                book_info = database.get_book_info(id)
                book_info_list.append(book_info)
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
    
    def onSaveMetadata(self):
        if self.bookInfo.isDataChanged:
            self.SaveMetadata()

    def SaveMetadata(self):
        self.wait()
        book_info_list = self.bookInfo.getData()
        for book_info in book_info_list:
            database.update_book_info(book_info)
        self.bookInfo.isDataChanged = False
        self.actionSave_metadata.setEnabled(False)
        
        self.bookList.updateRows()
        self.stopWait()
     
    def onRename(self):
        renameDialog = RenameDialog(self)
        if renameDialog.exec_():
            print('Ok')

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

    def closeEvent(self, e):
        self.exitApp()

    def onExit(self):
        self.close()

    def exitApp(self):
        config.ui_window_x = self.pos().x()
        config.ui_window_y = self.pos().y()
        config.ui_window_width = self.size().width()
        config.ui_window_height = self.size().height()
        config.ui_info_panel_visible = self.actionViewInfo_panel.isChecked()
        config.ui_filter_panel_visible = self.actionFilter_panel.isChecked()
        config.ui_auto_apply_filter = self.isAutoApplyFilter
        if self.actionViewInfo_panel.isChecked():
            config.ui_splitter_sizes = self.splitter.sizes()
        else:
            config.ui_splitter_sizes = self.prevSplitterSizes;
        
        config.save()
        database.clear()




