# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/designer/textviewdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ViewTextDialog(object):
    def setupUi(self, ViewTextDialog):
        ViewTextDialog.setObjectName("ViewTextDialog")
        ViewTextDialog.resize(580, 350)
        self.verticalLayout = QtWidgets.QVBoxLayout(ViewTextDialog)
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(ViewTextDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(ViewTextDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ViewTextDialog)
        self.buttonBox.accepted.connect(ViewTextDialog.accept) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ViewTextDialog)

    def retranslateUi(self, ViewTextDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewTextDialog.setWindowTitle(_translate("ViewTextDialog", "Dialog"))
