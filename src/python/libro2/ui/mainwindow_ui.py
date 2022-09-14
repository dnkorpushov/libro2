# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/designer/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(921, 465)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setContentsMargins(1, 0, 1, 1)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bookInfo = BookInfoPanel(self.frame)
        self.bookInfo.setMinimumSize(QtCore.QSize(200, 0))
        self.bookInfo.setBaseSize(QtCore.QSize(200, 0))
        self.bookInfo.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.bookInfo.setObjectName("bookInfo")
        self.verticalLayout_2.addWidget(self.bookInfo)
        self.bookList = BookTableView(self.splitter)
        self.bookList.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.bookList.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bookList.setMidLineWidth(0)
        self.bookList.setObjectName("bookList")
        self.verticalLayout.addWidget(self.splitter)
        self.frameFilter = QtWidgets.QFrame(self.centralwidget)
        self.frameFilter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frameFilter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameFilter.setObjectName("frameFilter")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frameFilter)
        self.horizontalLayout.setContentsMargins(16, 16, 16, 16)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frameFilter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textFilter = ButtonLineEdit(self.frameFilter)
        self.textFilter.setObjectName("textFilter")
        self.horizontalLayout.addWidget(self.textFilter)
        self.verticalLayout.addWidget(self.frameFilter)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 921, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = MainToolbar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setBaseSize(QtCore.QSize(0, 40))
        self.toolBar.setAutoFillBackground(False)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(22, 22))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionAdd_file = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/toolbar/plus-box.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_file.setIcon(icon)
        self.actionAdd_file.setIconVisibleInMenu(False)
        self.actionAdd_file.setShortcutVisibleInContextMenu(True)
        self.actionAdd_file.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionAdd_file.setObjectName("actionAdd_file")
        self.actionAdd_folder = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/toolbar/folder-plus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAdd_folder.setIcon(icon1)
        self.actionAdd_folder.setIconVisibleInMenu(False)
        self.actionAdd_folder.setPriority(QtWidgets.QAction.LowPriority)
        self.actionAdd_folder.setObjectName("actionAdd_folder")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setMenuRole(QtWidgets.QAction.QuitRole)
        self.actionExit.setIconVisibleInMenu(False)
        self.actionExit.setObjectName("actionExit")
        self.actionSelect_all = QtWidgets.QAction(MainWindow)
        self.actionSelect_all.setObjectName("actionSelect_all")
        self.actionRemove_selected_files = QtWidgets.QAction(MainWindow)
        self.actionRemove_selected_files.setObjectName("actionRemove_selected_files")
        self.actionViewInfo_panel = QtWidgets.QAction(MainWindow)
        self.actionViewInfo_panel.setCheckable(True)
        self.actionViewInfo_panel.setChecked(True)
        self.actionViewInfo_panel.setObjectName("actionViewInfo_panel")
        self.actionFilter_panel = QtWidgets.QAction(MainWindow)
        self.actionFilter_panel.setCheckable(True)
        self.actionFilter_panel.setChecked(True)
        self.actionFilter_panel.setPriority(QtWidgets.QAction.NormalPriority)
        self.actionFilter_panel.setObjectName("actionFilter_panel")
        self.actionRename = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/toolbar/swap-horizontal-bold.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRename.setIcon(icon2)
        self.actionRename.setIconVisibleInMenu(False)
        self.actionRename.setObjectName("actionRename")
        self.actionConvert = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/toolbar/file-send.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConvert.setIcon(icon3)
        self.actionConvert.setIconVisibleInMenu(False)
        self.actionConvert.setObjectName("actionConvert")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtWidgets.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionForum = QtWidgets.QAction(MainWindow)
        self.actionForum.setObjectName("actionForum")
        self.actionEdit_metadata = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/toolbar/pencil.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEdit_metadata.setIcon(icon4)
        self.actionEdit_metadata.setIconVisibleInMenu(False)
        self.actionEdit_metadata.setObjectName("actionEdit_metadata")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/toolbar/cog.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon5)
        self.actionSettings.setMenuRole(QtWidgets.QAction.PreferencesRole)
        self.actionSettings.setIconVisibleInMenu(False)
        self.actionSettings.setObjectName("actionSettings")
        self.actionRemove_all = QtWidgets.QAction(MainWindow)
        self.actionRemove_all.setObjectName("actionRemove_all")
        self.menuFile.addAction(self.actionAdd_file)
        self.menuFile.addAction(self.actionAdd_folder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionEdit_metadata)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRename)
        self.menuFile.addAction(self.actionConvert)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionSelect_all)
        self.menuEdit.addAction(self.actionRemove_selected_files)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionRemove_all)
        self.menuView.addAction(self.actionViewInfo_panel)
        self.menuView.addAction(self.actionFilter_panel)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionForum)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionAdd_file)
        self.toolBar.addAction(self.actionAdd_folder)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionEdit_metadata)
        self.toolBar.addAction(self.actionRename)
        self.toolBar.addAction(self.actionConvert)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)
        self.actionAdd_file.triggered.connect(MainWindow.onAddFiles) # type: ignore
        self.actionAdd_folder.triggered.connect(MainWindow.onAddFolder) # type: ignore
        self.actionExit.triggered.connect(MainWindow.onExit) # type: ignore
        self.actionSelect_all.triggered.connect(MainWindow.onSelectAll) # type: ignore
        self.actionRemove_selected_files.triggered.connect(MainWindow.onRemoveSelected) # type: ignore
        self.actionViewInfo_panel.toggled['bool'].connect(MainWindow.onViewInfoPanel) # type: ignore
        self.actionFilter_panel.toggled['bool'].connect(MainWindow.onViewFilterPanel) # type: ignore
        self.actionRename.triggered.connect(MainWindow.onRename) # type: ignore
        self.actionAbout_Qt.triggered.connect(MainWindow.onAboutQt) # type: ignore
        self.actionAbout.triggered.connect(MainWindow.onAbout) # type: ignore
        self.actionConvert.triggered.connect(MainWindow.onConvert) # type: ignore
        self.actionHelp.triggered.connect(MainWindow.onHelp) # type: ignore
        self.actionForum.triggered.connect(MainWindow.onForumLink) # type: ignore
        self.actionEdit_metadata.triggered.connect(MainWindow.onEditMetadata) # type: ignore
        self.actionSettings.triggered.connect(MainWindow.onSettings) # type: ignore
        self.actionRemove_all.triggered.connect(MainWindow.onRemoveAll) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Libro2"))
        self.label.setText(_translate("MainWindow", "Filter:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "Toolbar"))
        self.actionAdd_file.setText(_translate("MainWindow", "Add..."))
        self.actionAdd_file.setToolTip(_translate("MainWindow", "Add files"))
        self.actionAdd_file.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAdd_folder.setText(_translate("MainWindow", "Add folder..."))
        self.actionAdd_folder.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionSelect_all.setText(_translate("MainWindow", "Select all"))
        self.actionSelect_all.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionRemove_selected_files.setText(_translate("MainWindow", "Remove selected files"))
        self.actionRemove_selected_files.setShortcut(_translate("MainWindow", "Del"))
        self.actionViewInfo_panel.setText(_translate("MainWindow", "Info panel"))
        self.actionViewInfo_panel.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionFilter_panel.setText(_translate("MainWindow", "Filter panel"))
        self.actionFilter_panel.setShortcut(_translate("MainWindow", "F3"))
        self.actionRename.setText(_translate("MainWindow", "Rename..."))
        self.actionRename.setToolTip(_translate("MainWindow", "Rename selected files"))
        self.actionRename.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionConvert.setText(_translate("MainWindow", "Convert..."))
        self.actionConvert.setToolTip(_translate("MainWindow", "Convert selected files"))
        self.actionConvert.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionAbout.setText(_translate("MainWindow", "About..."))
        self.actionAbout_Qt.setText(_translate("MainWindow", "About Qt..."))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionForum.setText(_translate("MainWindow", "Forum"))
        self.actionEdit_metadata.setText(_translate("MainWindow", "Edit..."))
        self.actionEdit_metadata.setIconText(_translate("MainWindow", "Edit"))
        self.actionEdit_metadata.setToolTip(_translate("MainWindow", "Edit metadata for selected files"))
        self.actionEdit_metadata.setShortcut(_translate("MainWindow", "Ctrl+E"))
        self.actionSettings.setText(_translate("MainWindow", "Settings..."))
        self.actionRemove_all.setText(_translate("MainWindow", "Remove all"))
        self.actionRemove_all.setShortcut(_translate("MainWindow", "Shift+Del"))
from .bookinfopanel import BookInfoPanel
from .booktableview import BookTableView
from .customcontrols import ButtonLineEdit
from .maintoolbar import MainToolbar
from . import resources_rc
