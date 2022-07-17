from functools import partial
import os
import sys
import webbrowser

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QMenu, QAction, QWidget, QLineEdit
from PyQt5.QtCore import Qt, QPoint, QCoreApplication, QTimer, QEvent
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette

from .mainwindow_ui import Ui_MainWindow
from .addfilesdialog import AddFilesDialog
from .renamedialog import RenameDialog
from .movefilesdialog import MoveFilesDialog
from .textviewdialog import TextViewDialog
from .aboutdialog import AboutDialog
from .convertdialog import ConvertDialog
from .convertfilesdialog import ConvertFilesDialog
from .runplugindialog import RunPluginDialog

import config
import database
from plugin_collection import PluginCollection

settings = config.settings

_t = QCoreApplication.translate

HELP_LINK = 'https://github.com/dnkorpushov/libro2/wiki'
FORUM_LINK = 'https://4pda.to/forum/index.php?showtopic=947577'

class MainWindow (QMainWindow, Ui_MainWindow):
    def __init__(self):
        config.init()
        config.load()
        database.init()

        self.prevSplitterSizes = None
        self.isAutoApplyFilter = True

        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon(':/icons/libro2_48px.png'))
        
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
        
        self.customFilterLineEdit = QLineEdit()
        action = self.customFilterLineEdit.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        action.triggered.connect(self.onToolFilterMenu)
        self.customFilterLineEdit.textChanged.connect(self.setFilterOnTextChanged)
        self.customFilterLineEdit.returnPressed.connect(self.setFilterOnReturnPressed)

        self.textFilter.setLineEdit(self.customFilterLineEdit)

        self.bookInfo.clear()

        self.bookList.setColumnsWidth(settings.ui_columns_width)
        self.bookList.setColumnsOrder(settings.ui_columns_order)
        self.bookList.setHiddenColumns(settings.ui_hidden_columns)
        self.bookList.setHiddenColumnsWidth(settings.ui_hidden_columns_width)
        self.bookList.selectionModel().selectionChanged.connect(self.onBookListSelectionChanged)

        self.bookList.installEventFilter(self)
        self.bookList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookList.customContextMenuRequested.connect(self.onBookListContextMenu)

        self.toolBar.visibilityChanged.connect(self.onToobarVisibilityChange)
        self.toolBar.setVisible(settings.ui_toolbar_visible)
        if settings.ui_toolbar_icon_size == 'small':
            self.onToolbarIconSmall()
        else:
            self.onToolbarIconLarge()
        self.actionsSetEnabled(False)
        self.actionSave_metadata.setEnabled(False)
        self.bookInfo.dataChanged.connect(self.OnBookInfoDataChanged)

        self.setPlatformUI()

        self.bookInfo.mainInfoCollapsed = settings.ui_main_info_collapsed
        self.bookInfo.publishInfoCollapsed = settings.ui_publish_info_collapsed
        self.bookInfo.coverInfoCollapsed = settings.ui_cover_info_collapsed
        self.bookInfo.descriptionInfoCollapsed = settings.ui_description_info_collapsed

        QTimer.singleShot(1, self.loadFilesFromCommandLine)

        # Init plugins
        self.pluginCollection = PluginCollection()
        self.initPluginsMenu()


    def runPlugin(self, action):
        plugin = action.data()

        book_info_list = self.getSelectedBookList()
        if len(book_info_list):
            self.wait()
       
            runPluginDialog = RunPluginDialog(self, plugin, book_info_list)
            runPluginDialog.exec()

            self.bookList.updateRows()
            self.stopWait()

            errors = runPluginDialog.getErrors()
            if len(errors) > 0:
                errorDialog = TextViewDialog(self, errors)
                errorDialog.exec()
                        
    def initPluginsMenu(self):
        for plugin in self.pluginCollection.plugins():
            try:
                action = self.menuTools.addAction(plugin.description())
                action.setData(plugin)
                action.triggered.connect(partial(self.runPlugin, action))
            except Exception as e:
                print(e)
        self.menuTools.addSeparator()
        action = self.menuTools.addAction(_t('main', 'Reload plugins'))
        action.triggered.connect(self.reloadPlugins)

        if len(self.pluginCollection.errors) > 0:
            errorDialog = TextViewDialog(self, self.pluginCollection.errors)
            errorDialog.exec()

    def reloadPlugins(self):
        self.menuTools.clear()
        self.pluginCollection.reload_plugins()
        self.initPluginsMenu()
        

    def onBookListContextMenu(self, point):
        menu = QMenu()
        menu.addAction(self.actionRename)
        menu.addAction(self.actionConvert)
        menu.addSeparator()
        menu.addAction(self.actionRemove_selected_files)

        menu.exec(self.bookList.viewport().mapToGlobal(point))

    def eventFilter(self, source, event):
        if source is self.bookList:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.accept()
                    return True
            elif event.type() == QEvent.Drop:
                urlList = [x.toLocalFile() for x in event.mimeData().urls()]
                self.addFilesAndDirs(urlList)
                event.accept()
                return True
        return QWidget.eventFilter(self, source, event)

    def addFilesAndDirs(self, list_to_load):
        files_to_load = []
        for item in list_to_load:
            if os.path.isdir(item):
                for root, dir, files in os.walk(item):
                    for file in files:
                        files_to_load.append(os.path.join(root, file))
            elif os.path.isfile(item):
                files_to_load.append(item)

        if len(files_to_load) > 0:
            self.AddFiles(files_to_load)

    def loadFilesFromCommandLine(self):
        if len(sys.argv) > 1:
            self.addFilesAndDirs(sys.argv[1:])

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
                                              caption=_t('main', 'Add files'), 
                                              directory=settings.add_files_last_selected,
                                              filter=_t('main', 'Ebook files (*.fb2 *.fb2.zip *.epub);;All files (*.*)'))
        if len(result[0]) > 0:
            self.AddFiles(result[0])
            for file in result[0]:
                (settings.add_files_last_selected, _) = os.path.split(file)

    def onAddFolder(self):
        fileList = []
        folder = QFileDialog.getExistingDirectory(self,
                                                  caption=_t('main', 'Add folder'),
                                                  directory=settings.add_folder_last_selected)
        if folder:
            settings.add_folder_last_selected = folder
            for root, dir, files in os.walk(folder):
                for file in files:
                    fileList.append(os.path.join(root, file))
        
            self.AddFiles(fileList)

    def AddFiles(self, files):
        # Remove unsupported files from list
        files = [file for file in files if file.lower().endswith(('.fb2', '.fb2.zip', '.epub'))]
        if len(files) > 0:
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
            if QMessageBox.question(self, 'Libro2', _t('main', 'Save changes?')) == QMessageBox.Yes:
                self.SaveMetadata()

        book_info_list = self.getSelectedBookList()

        self.bookInfo.clear()

        if len(book_info_list) > 0:
            self.actionsSetEnabled(True)
            self.bookInfo.setData(book_info_list)
        else:
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
            renameDialog.authorFormatList = settings.rename_author_template_list
            renameDialog.filenameFormatList = settings.rename_filename_template_list
            renameDialog.authorFormat = settings.rename_author_format
            renameDialog.filenameFormat = settings.rename_filename_format
            renameDialog.deleteSourceFiles = settings.rename_delete_source_files
            renameDialog.overwriteExistingFiles = settings.rename_overwrite
            renameDialog.backupBeforeRename = settings.rename_backup
            

            if renameDialog.exec_():
                self.wait()
                moveFilesDialog = MoveFilesDialog(self, 
                                                  book_info_list=book_info_list,
                                                  filename_format=renameDialog.filenameFormat, 
                                                  author_format=renameDialog.authorFormat,
                                                  delete_src=renameDialog.deleteSourceFiles,
                                                  backup_src=renameDialog.backupBeforeRename,
                                                  overwrite_exists=renameDialog.overwriteExistingFiles)
                moveFilesDialog.exec()
                self.bookList.updateRows()
                self.stopWait()
                        
                
                settings.rename_delete_source_files = renameDialog.deleteSourceFiles
                settings.rename_overwrite = renameDialog.overwriteExistingFiles
                settings.rename_backup = renameDialog.backupBeforeRename

                errors = moveFilesDialog.getErrors()
                if len(errors) > 0:
                    errorDialog = TextViewDialog(self, errors)
                    errorDialog.exec()

            settings.rename_author_format = renameDialog.authorFormat
            settings.rename_filename_format = renameDialog.filenameFormat
            settings.rename_author_template_list = renameDialog.authorFormatList
            settings.rename_filename_template_list = renameDialog.filenameFormatList

    def onConvert(self):
        convertDialog = ConvertDialog(self)
        convertDialog.outputFormat = settings.convert_output_format
        convertDialog.outputPath = settings.convert_output_path
        convertDialog.overwrite = settings.convert_overwrite
        convertDialog.stk = settings.convert_stk
        convertDialog.converterPath = settings.convert_converter_path
        convertDialog.converterConfig = settings.convert_converter_config

        if convertDialog.exec_():
            book_info_list = self.getSelectedBookList()
            convertProgress = ConvertFilesDialog(self, 
                                                 book_info_list=book_info_list,
                                                 out_format=convertDialog.outputFormat,
                                                 out_path=convertDialog.outputPath,
                                                 overwrite=convertDialog.overwrite,
                                                 stk = convertDialog.stk,
                                                 converter_path=convertDialog.converterPath,
                                                 converter_config=convertDialog.converterConfig)
            convertProgress.exec()

            if len(convertProgress.errors) > 0:
                errorDialog = TextViewDialog(self, convertProgress.errors)
                errorDialog.exec()
            
            settings.convert_output_format = convertDialog.outputFormat
            settings.convert_output_path = convertDialog.outputPath
            settings.convert_overwrite = convertDialog.overwrite 
            settings.convert_stk = convertDialog.stk
            settings.convert_converter_path = convertDialog.converterPath
            settings.convert_converter_config = convertDialog.converterConfig

    def onToolFilterMenu(self):
        actionList = {
            'title': _t('main', 'Title'),
            'authors': _t('main', 'Author'),
            'series': _t('main', 'Series'),
            'tags': _t('main', 'Tags'),
            'lang': _t('main', 'Lang'),
            'translators': _t('main', 'Translator'),
            'type': _t('main', 'Type'),
            'file': _t('main', 'File') 
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
        actionItem = QAction(_t('main', 'Auto-apply filter'), parent=menu, checkable=True, checked=self.isAutoApplyFilter)
        actionItem.setData('AutoApplyFilter')
        menu.addAction(actionItem)
        
        menu_x = -1 * menu.sizeHint().width() + self.textFilter.width()
        menu_y = -1 * menu.sizeHint().height() + self.textFilter.height()
        
        action = menu.exec_(self.textFilter.mapToGlobal(QPoint(menu_x , menu_y)))
        if action:
            if action.data() == 'AutoApplyFilter':
                self.isAutoApplyFilter = not self.isAutoApplyFilter
            elif action.data() in ('AND', 'OR'):
                self.textFilter.setCurrentText(self.textFilter.currentText() + ' {} '.format(action.data()))
            else:
                self.textFilter.setCurrentText(self.textFilter.currentText() + ' {}:'.format(action.data()))
            self.textFilter.setFocus(True)
 
    def onToolbarIconLarge(self):
        self.toolBar.setLargeIcons()
        self.actionToolbarIconsLarge.setChecked(True)
        self.actionToolbarIconSmall.setChecked(False)

    def onToolbarIconSmall(self):
        self.toolBar.setSmallIcons()
        self.actionToolbarIconsLarge.setChecked(False)
        self.actionToolbarIconSmall.setChecked(True)

    def onToobarVisibilityChange(self):
        self.actionViewToolbar.setChecked(self.toolBar.isVisible())

    def setPlatformUI(self):
        if sys.platform == 'win32':
            font = QFont('Segoe UI', 9)
            self.label.setFont(font)
            self.textFilter.setFont(font)
            self.toolBar.setStyleSheet('#toolBar { border-bottom: 1px solid #bfbfbf; border-left: 1px solid #ffffff; border-right: 1px solid #ffffff;  background-color: #f7f7f7}')

            self.frameFilter.setStyleSheet('#frameFilter {border-top: 1px solid #bfbfbf;}')
            self.splitter.setStyleSheet('QSplitter::handle { background: #bfbfbf; }')
        elif sys.platform == 'darwin':
            self.setUnifiedTitleAndToolBarOnMac(True)
            self.frameFilter.setStyleSheet('#frameFilter {border-top: 1px solid #bfbfbf;}')
            self.splitter.setStyleSheet('QSplitter::handle { background: #bfbfbf; }')
        # else:
        #     self.toolBar.setStyleSheet('QToolBar { border: 0px }')
            
    def onHelp(self):
        browser = webbrowser.get()
        browser.open_new_tab(HELP_LINK)
    
    def onForumLink(self):
        browser = webbrowser.get()
        browser.open_new_tab(FORUM_LINK)

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
        settings.ui_toolbar_icon_size = 'small' if self.actionToolbarIconSmall.isChecked() else 'large'

        settings.ui_main_info_collapsed = self.bookInfo.mainInfoCollapsed
        settings.ui_publish_info_collapsed = self.bookInfo.publishInfoCollapsed
        settings.ui_cover_info_collapsed = self.bookInfo.coverInfoCollapsed
        settings.ui_description_info_collapsed = self.bookInfo.descriptionInfoCollapsed

        if self.actionViewInfo_panel.isChecked():
            settings.ui_splitter_sizes = self.splitter.sizes()
        else:
            settings.ui_splitter_sizes = self.prevSplitterSizes;

        config.save()
        database.close()
        config.delete_temp_dir()




