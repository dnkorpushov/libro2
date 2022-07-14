# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\designer\convertdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConvertDialog(object):
    def setupUi(self, ConvertDialog):
        ConvertDialog.setObjectName("ConvertDialog")
        ConvertDialog.resize(483, 297)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ConvertDialog)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(ConvertDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboFormat = QtWidgets.QComboBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboFormat.sizePolicy().hasHeightForWidth())
        self.comboFormat.setSizePolicy(sizePolicy)
        self.comboFormat.setObjectName("comboFormat")
        self.comboFormat.addItem("")
        self.comboFormat.addItem("")
        self.comboFormat.addItem("")
        self.comboFormat.addItem("")
        self.verticalLayout.addWidget(self.comboFormat)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textOutputDir = QtWidgets.QLineEdit(self.tab)
        self.textOutputDir.setObjectName("textOutputDir")
        self.verticalLayout.addWidget(self.textOutputDir)
        self.checkOverwrite = QtWidgets.QCheckBox(self.tab)
        self.checkOverwrite.setObjectName("checkOverwrite")
        self.verticalLayout.addWidget(self.checkOverwrite)
        self.checkStk = QtWidgets.QCheckBox(self.tab)
        self.checkStk.setObjectName("checkStk")
        self.verticalLayout.addWidget(self.checkStk)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(4, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.textConverterPath = QtWidgets.QLineEdit(self.tab_2)
        self.textConverterPath.setObjectName("textConverterPath")
        self.verticalLayout_3.addWidget(self.textConverterPath)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.textConverterConfig = QtWidgets.QLineEdit(self.tab_2)
        self.textConverterConfig.setObjectName("textConverterConfig")
        self.verticalLayout_3.addWidget(self.textConverterConfig)
        self.labelEditConfig = QtWidgets.QLabel(self.tab_2)
        self.labelEditConfig.setObjectName("labelEditConfig")
        self.verticalLayout_3.addWidget(self.labelEditConfig)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.labelDownloadConverter = QtWidgets.QLabel(self.tab_2)
        self.labelDownloadConverter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelDownloadConverter.setObjectName("labelDownloadConverter")
        self.verticalLayout_3.addWidget(self.labelDownloadConverter)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConvertDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(ConvertDialog)
        self.tabWidget.setCurrentIndex(1)
        self.buttonBox.accepted.connect(ConvertDialog.accept)
        self.buttonBox.rejected.connect(ConvertDialog.reject)
        self.labelEditConfig.linkActivated['QString'].connect(ConvertDialog.onEditConfig)
        self.labelDownloadConverter.linkActivated['QString'].connect(ConvertDialog.onDownloadConverter)
        QtCore.QMetaObject.connectSlotsByName(ConvertDialog)

    def retranslateUi(self, ConvertDialog):
        _translate = QtCore.QCoreApplication.translate
        ConvertDialog.setWindowTitle(_translate("ConvertDialog", "Convert"))
        self.label.setText(_translate("ConvertDialog", "Output format"))
        self.comboFormat.setItemText(0, _translate("ConvertDialog", "epub"))
        self.comboFormat.setItemText(1, _translate("ConvertDialog", "kepub"))
        self.comboFormat.setItemText(2, _translate("ConvertDialog", "mobi"))
        self.comboFormat.setItemText(3, _translate("ConvertDialog", "azw3"))
        self.label_2.setText(_translate("ConvertDialog", "Output folder"))
        self.checkOverwrite.setText(_translate("ConvertDialog", "Overwrite existing files"))
        self.checkStk.setText(_translate("ConvertDialog", "Send to Kindle"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ConvertDialog", "Convert"))
        self.label_3.setText(_translate("ConvertDialog", "Path to fb2c executable"))
        self.label_4.setText(_translate("ConvertDialog", "fb2c config file"))
        self.labelEditConfig.setText(_translate("ConvertDialog", "<html><head/><body><p><a href=\"https://null\"><span style=\" text-decoration: underline; color:#0000ff;\">Edit config file</span></a></p></body></html>"))
        self.labelDownloadConverter.setText(_translate("ConvertDialog", "<html><head/><body><p><a href=\"https://github.com/rupor-github/fb2converter/releases/\"><span style=\" text-decoration: underline; color:#0000ff;\">Download fb2converter</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ConvertDialog", "fb2c"))
