from functools import partial
import os
import sys
import webbrowser
import traceback

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QMenu, QAction, QWidget
from PyQt5.QtCore import Qt, QPoint, QCoreApplication, QTimer, QEvent
from PyQt5.QtGui import QIcon, QKeySequence

from .mainwindow_ui import Ui_MainWindow
from .addfilesdialog import AddFilesDialog
from .renamedialog import RenameDialog
from .movefilesdialog import MoveFilesDialog
from .textviewdialog import TextViewDialog
from .aboutdialog import AboutDialog
from .convertdialog import ConvertDialog
from .convertfilesdialog import ConvertFilesDialog
from .runplugindialog import RunPluginDialog
from .editdialog import EditDialog
from .settingsdialog import SettingsDialog

import config
import database
from plugin_collection import PluginCollection
from .pluginform import PluginForm

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
        self.actionsEnabled = False

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
        
        self.textFilter.clicked.connect(self.onToolFilterMenu)
        self.textFilter.textChanged.connect(self.setFilterOnTextChanged)
        self.textFilter.returnPressed.connect(self.setFilterOnReturnPressed)

        self.bookInfo.clear()

        self.bookList.setColumnsWidth(settings.ui_columns_width)
        self.bookList.setColumnsOrder(settings.ui_columns_order)
        self.bookList.setHiddenColumns(settings.ui_hidden_columns)
        self.bookList.setHiddenColumnsWidth(settings.ui_hidden_columns_width)
        self.bookList.selectionModel().selectionChanged.connect(self.onBookListSelectionChanged)

        self.bookList.installEventFilter(self)
        self.bookList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.bookList.customContextMenuRequested.connect(self.onBookListContextMenu)

        self.setPlatformUI()

        QTimer.singleShot(1, self.loadFilesOnStartup)

        # Init plugins
        self.pluginCollection = PluginCollection()
        self.initPluginsMenu()

        self.ui_scale = self.screen().logicalDotsPerInchX() / 96
        
        self.toolBar.setIconScale(self.ui_scale)
        self.bookInfo.setScaleFactor(self.ui_scale)

        self.actionsSetEnabled()

    def runPlugin(self, action):
        plugin = action.data()
        run_plugin = True

        book_info_list = self.getSelectedBookList()
        if len(book_info_list):
            try:
                pluginForm = PluginForm(self, plugin.params(), title=plugin.title(), scale_factor=self.ui_scale)
                if pluginForm.exec_():
                    plugin_params = pluginForm.getParams()
                    plugin.set_params(plugin_params)
                else:
                    run_plugin = False
            except:
                errorDialog = TextViewDialog(self, [{ 'src': None, 'dest': None, 'error': traceback.format_exc()}], self.ui_scale)
                errorDialog.exec()

            if run_plugin:
                self.wait()
        
                runPluginDialog = RunPluginDialog(self, plugin, book_info_list, self.ui_scale)
                runPluginDialog.exec()

                self.bookList.updateRows()
                self.stopWait()

                errors = runPluginDialog.getErrors()
                if len(errors) > 0:
                    errorDialog = TextViewDialog(self, errors, self.ui_scale)
                    errorDialog.exec()
                        
    def initPluginsMenu(self):
        for plugin in self.pluginCollection.plugins():
            try:
                action = self.menuTools.addAction(plugin.title())
                action.setData(plugin)
                if plugin.hotkey():
                    action.setShortcut(QKeySequence(plugin.hotkey()))
                action.triggered.connect(partial(self.runPlugin, action))
            except Exception as e:
                print(e)
        self.menuTools.addSeparator()
        action = self.menuTools.addAction(_t('main', 'Reload plugins'))
        action.triggered.connect(self.reloadPlugins)

        if len(self.pluginCollection.errors) > 0:
            errorDialog = TextViewDialog(self, self.pluginCollection.errors, self.ui_scale)
            errorDialog.exec()

    def reloadPlugins(self):
        self.menuTools.clear()
        self.pluginCollection.reload_plugins()
        self.initPluginsMenu()
        self.actionsSetEnabled()
        
    def onBookListContextMenu(self, point):
        menu = QMenu()
        menu.addAction(self.actionEdit_metadata)
        menu.addAction(self.actionRename)
        menu.addAction(self.actionConvert)
        menu.addSeparator()

        for plugin in self.pluginCollection.plugins():
            try:
                if plugin.is_context_menu():
                    action = menu.addAction(plugin.title())
                    action.setData(plugin)
                    if plugin.hotkey():
                        action.setShortcut(QKeySequence(plugin.hotkey()))
                    action.triggered.connect(partial(self.runPlugin, action))
            except Exception as e:
                print(e)

        menu.addSeparator()
        menu.addAction(self.actionRemove_selected_files)
        menu.addAction(self.actionRemove_all)

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

    def loadFilesOnStartup(self):
        if len(sys.argv) > 1:
            self.addFilesAndDirs(sys.argv[1:])
        else:
            if settings.is_open_folder_on_start:
                if settings.open_folder_on_start:
                    self.addFilesAndDirs([settings.open_folder_on_start])

    def setFilterOnTextChanged(self):
        if self.isAutoApplyFilter:
            self.setFilter()

    def setFilterOnReturnPressed(self):
        if not self.isAutoApplyFilter:
            self.setFilter()

    def setFilter(self):
        self.bookList.setFilter(self.textFilter.text())  

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
            loadFilesDialog = AddFilesDialog(self, files, self.ui_scale)
            loadFilesDialog.exec()
            self.bookList.updateRows()
            errors = loadFilesDialog.getErrors()
            if len(errors) > 0:
                errorDialog = TextViewDialog(self, errors, self.ui_scale)
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
        book_info_list = self.getSelectedBookList()
        self.bookInfo.clear()

        if len(book_info_list) > 0:
            self.actionsEnabled = True
            self.bookInfo.setData(book_info_list)
        else:
            self.actionsEnabled = False

        self.actionsSetEnabled()

    def actionsSetEnabled(self):
        self.actionRename.setEnabled(self.actionsEnabled)
        self.actionConvert.setEnabled(self.actionsEnabled)
        self.actionEdit_metadata.setEnabled(self.actionsEnabled)

        for action in self.menuTools.actions():
            if action.isSeparator():
                break
            else:
                action.setEnabled(self.actionsEnabled)

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
            self.splitter.setHandleWidth(1)
            self.splitter.setSizes(self.prevSplitterSizes)
        else:
            self.prevSplitterSizes = self.splitter.sizes()
            self.splitter.setHandleWidth(0)
            self.splitter.setSizes((0, 1))

    def onRename(self):
        book_info_list = self.getSelectedBookList()
        if len(book_info_list):
            renameDialog = RenameDialog(self, self.ui_scale)
            renameDialog.bookList = book_info_list
            renameDialog.authorFormatList = settings.rename_author_template_list
            renameDialog.filenameFormatList = settings.rename_filename_template_list
            renameDialog.authorFormat = settings.rename_author_format
            renameDialog.filenameFormat = settings.rename_filename_format
            renameDialog.deleteSourceFiles = settings.rename_delete_source_files
            renameDialog.overwriteExistingFiles = settings.rename_overwrite
            renameDialog.backupBeforeRename = settings.rename_backup
            renameDialog.renameInSourceFolder = settings.rename_in_source_folder
            renameDialog.renameMoveToFolder = settings.rename_move_to_folder
            
            if renameDialog.exec_():
                self.wait()
                moveFilesDialog = MoveFilesDialog(self, 
                                                  book_info_list=book_info_list,
                                                  filename_format=renameDialog.filenameFormat, 
                                                  author_format=renameDialog.authorFormat,
                                                  delete_src=renameDialog.deleteSourceFiles,
                                                  backup_src=renameDialog.backupBeforeRename,
                                                  overwrite_exists=renameDialog.overwriteExistingFiles,
                                                  rename_in_source_folder=renameDialog.renameInSourceFolder,
                                                  move_to_folder=renameDialog.renameMoveToFolder)
                moveFilesDialog.exec()
                self.bookList.updateRows()
                self.stopWait()
                        
                settings.rename_delete_source_files = renameDialog.deleteSourceFiles
                settings.rename_overwrite = renameDialog.overwriteExistingFiles
                settings.rename_backup = renameDialog.backupBeforeRename
                settings.rename_in_source_folder = renameDialog.renameInSourceFolder
                settings.rename_move_to_folder = renameDialog.renameMoveToFolder

                errors = moveFilesDialog.getErrors()
                if len(errors) > 0:
                    errorDialog = TextViewDialog(self, errors, self.ui_scale)
                    errorDialog.exec()

            settings.rename_author_format = renameDialog.authorFormat
            settings.rename_filename_format = renameDialog.filenameFormat
            settings.rename_author_template_list = renameDialog.authorFormatList
            settings.rename_filename_template_list = renameDialog.filenameFormatList

    def onConvert(self):
        if (not settings.convert_converter_path or 
                (settings.convert_converter_path and not os.path.exists(settings.convert_converter_path))):
            QMessageBox.critical(self, 'Libro2', _t('main', 'Check settings for fb2converter!'))
            
            return
       
        convertDialog = ConvertDialog(self, self.ui_scale)
        convertDialog.outputFormat = settings.convert_output_format
        convertDialog.outputPath = settings.convert_output_path
        convertDialog.overwrite = settings.convert_overwrite
        convertDialog.stk = settings.convert_stk
       
        if convertDialog.exec_():
            book_info_list = self.getSelectedBookList()
            convertProgress = ConvertFilesDialog(self, 
                                                 book_info_list=book_info_list,
                                                 out_format=convertDialog.outputFormat,
                                                 out_path=convertDialog.outputPath,
                                                 overwrite=convertDialog.overwrite,
                                                 stk = convertDialog.stk,
                                                 debug=convertDialog.debug,
                                                 converter_path=settings.convert_converter_path,
                                                 converter_config=settings.convert_converter_config,
                                                 scale_factor=self.ui_scale)
            convertProgress.exec()

            if len(convertProgress.errors) > 0:
                errorDialog = TextViewDialog(self, convertProgress.errors, self.ui_scale)
                errorDialog.exec()
            
            settings.convert_output_format = convertDialog.outputFormat
            settings.convert_output_path = convertDialog.outputPath
            settings.convert_overwrite = convertDialog.overwrite 
            settings.convert_stk = convertDialog.stk
         
    def onEditMetadata(self):
        book_info_list = self.getSelectedBookList()
        if len(book_info_list) > 0:
            editDialog = EditDialog(self, book_info_list, self.ui_scale)

            if editDialog.exec():
                self.wait()
                
                book_info_list = editDialog.getData()
                errors = []
                for book_info in book_info_list:
                    try:
                        database.update_book_info(book_info)
                    except Exception as e:
                        errors.append({ 'src': book_info.file, 'dest': None, 'error': str(e) })
        
                self.bookList.updateRows()
                self.stopWait()

                if len(errors) > 0:
                    errorDialog = TextViewDialog(self, errors, self.ui_scale)
                    errorDialog.exec()

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
        menu_y = -1 * menu.sizeHint().height() - 2
        
        action = menu.exec_(self.textFilter.mapToGlobal(QPoint(menu_x , menu_y)))
        if action:
            if action.data() == 'AutoApplyFilter':
                self.isAutoApplyFilter = not self.isAutoApplyFilter
            elif action.data() in ('AND', 'OR'):
                self.textFilter.setText(self.textFilter.text() + ' {} '.format(action.data()))
            else:
                self.textFilter.setText(self.textFilter.text() + ' {}:'.format(action.data()))
            self.textFilter.setFocus(True)
 
    def setPlatformUI(self):
        self.frameFilter.setStyleSheet('''
            #frameFilter {
                border-top: 1px solid #bfbfbf;
            }
        ''')
        self.splitter.setStyleSheet('''
            QSplitter::handle { 
                background: #bfbfbf; 
            }
        ''')
        if sys.platform == 'win32':
            self.toolBar.setStyleSheet('''
                #toolBar { 
                    padding:4px; 
                    border-bottom: 1px solid #bfbfbf; 
                    border-left: 1px solid #ffffff; 
                    border-right: 1px solid #ffffff;  
                    background-color: #f7f7f7
                } 
            ''')
        
        elif sys.platform == 'darwin':
            self.toolBar.setStyleSheet('''
                #toolBar {
                    padding: 4px;
                }
            ''')
            self.setUnifiedTitleAndToolBarOnMac(True)
            self.frameFilter.layout().setContentsMargins(8, 8, 8, 8)
        else:
            self.toolBar.setStyleSheet('''
                #toolBar { 
                    padding: 2px;
                    border-bottom: 1px solid #bfbfbf; 
                    border-left: 1px solid #ffffff; 
                    border-right: 1px solid #ffffff;  
                    background-color: #f7f7f7}
            ''')
            
    def onSettings(self):
        settingsDialog = SettingsDialog(self, self.ui_scale)
        settingsDialog.isOpenFolderOnStart = settings.is_open_folder_on_start
        settingsDialog.openFolderOnStart = settings.open_folder_on_start
        settingsDialog.converterPath = settings.convert_converter_path
        settingsDialog.converterConfig = settings.convert_converter_config

        if settingsDialog.exec_():
            settings.is_open_folder_on_start = settingsDialog.isOpenFolderOnStart
            settings.open_folder_on_start = settingsDialog.openFolderOnStart
            settings.convert_converter_path = settingsDialog.converterPath
            settings.convert_converter_config = settingsDialog.converterConfig

    def onRemoveAll(self):
        self.wait()
        self.bookList.removeAll()
        if self.bookList.model().rowCount() == 0:
            self.bookInfo.clear()
        self.stopWait()

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
        database.close()
        config.delete_temp_dir()
