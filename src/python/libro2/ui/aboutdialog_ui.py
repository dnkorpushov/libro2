# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src\designer\aboutdialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(410, 230)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AboutDialog.sizePolicy().hasHeightForWidth())
        AboutDialog.setSizePolicy(sizePolicy)
        AboutDialog.setMinimumSize(QtCore.QSize(0, 0))
        AboutDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutDialog)
        self.verticalLayout.setContentsMargins(12, 12, 12, 12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label.setBaseSize(QtCore.QSize(-1, 0))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/libro2_48px.png"))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelName = QtWidgets.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelName.setFont(font)
        self.labelName.setObjectName("labelName")
        self.verticalLayout_2.addWidget(self.labelName)
        self.labelAuthor = QtWidgets.QLabel(AboutDialog)
        self.labelAuthor.setObjectName("labelAuthor")
        self.verticalLayout_2.addWidget(self.labelAuthor)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.labelAppIcon = QtWidgets.QLabel(AboutDialog)
        self.labelAppIcon.setTextFormat(QtCore.Qt.RichText)
        self.labelAppIcon.setObjectName("labelAppIcon")
        self.verticalLayout.addWidget(self.labelAppIcon)
        self.labelRuporCredits = QtWidgets.QLabel(AboutDialog)
        self.labelRuporCredits.setTextFormat(QtCore.Qt.RichText)
        self.labelRuporCredits.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelRuporCredits.setObjectName("labelRuporCredits")
        self.verticalLayout.addWidget(self.labelRuporCredits)
        self.labelNewVersion = QtWidgets.QLabel(AboutDialog)
        self.labelNewVersion.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelNewVersion.setObjectName("labelNewVersion")
        self.verticalLayout.addWidget(self.labelNewVersion)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(AboutDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)
        self.labelRuporCredits.linkActivated['QString'].connect(AboutDialog.openLink)
        self.labelNewVersion.linkActivated['QString'].connect(AboutDialog.openLink)
        self.labelAppIcon.linkActivated['QString'].connect(AboutDialog.openLink)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About Libro2"))
        self.labelName.setText(_translate("AboutDialog", "Libro2 v1.0"))
        self.labelAuthor.setText(_translate("AboutDialog", "Written by dnk_dz"))
        self.labelAppIcon.setText(_translate("AboutDialog", "<html><head/><body><p>App icon by <a href=\"https://icon-icons.com/users/5C4aDHDZ0aEGLnypl9KyW/icon-sets/\"><span style=\" text-decoration: underline; color:#0000ff;\">Nick Frost and Greg Lapin</span></a></p></body></html>"))
        self.labelRuporCredits.setText(_translate("AboutDialog", "<html><head/><body><p>Special sanks to <a href=\"https://github.com/rupor-github\">rupor</a> for <a href=\"https://github.com/rupor-github/fb2converter\">fb2converter</a> and </span><a href=\"https://github.com/rupor-github/fb2mobi\">fb2mobi</a></p></body></html>"))
        self.labelNewVersion.setText(_translate("AboutDialog", "<html><head/><body><p>Check new version <a href=\"https://github.com/dnkorpushov/libro2/releases\">here</a></p></body></html>"))
from . import resources_rc
