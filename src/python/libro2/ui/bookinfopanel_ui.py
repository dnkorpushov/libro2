# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/designer/bookinfopanel.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BookInfoPanel(object):
    def setupUi(self, BookInfoPanel):
        BookInfoPanel.setObjectName("BookInfoPanel")
        BookInfoPanel.resize(301, 770)
        BookInfoPanel.setMinimumSize(QtCore.QSize(200, 0))
        BookInfoPanel.setBaseSize(QtCore.QSize(200, 0))
        BookInfoPanel.setFocusPolicy(QtCore.Qt.StrongFocus)
        BookInfoPanel.setStyleSheet("QWidget { background-color #f7f7f7\n"
" }r")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(BookInfoPanel)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(BookInfoPanel)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 301, 770))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(12, 12, 12, 6)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.title.setWordWrap(True)
        self.title.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.series = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setItalic(False)
        self.series.setFont(font)
        self.series.setWordWrap(True)
        self.series.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.series.setObjectName("series")
        self.verticalLayout.addWidget(self.series)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.author = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.author.setWordWrap(True)
        self.author.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.author.setObjectName("author")
        self.verticalLayout.addWidget(self.author)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.cover = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.cover.setObjectName("cover")
        self.verticalLayout.addWidget(self.cover)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem3)
        self.labelTags = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTags.setFont(font)
        self.labelTags.setObjectName("labelTags")
        self.verticalLayout.addWidget(self.labelTags)
        self.tags = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.tags.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.tags.setWordWrap(True)
        self.tags.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.tags.setObjectName("tags")
        self.verticalLayout.addWidget(self.tags)
        self.spacerTags = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.spacerTags.setMaximumSize(QtCore.QSize(16777215, 10))
        self.spacerTags.setText("")
        self.spacerTags.setObjectName("spacerTags")
        self.verticalLayout.addWidget(self.spacerTags)
        self.labelLang = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelLang.setFont(font)
        self.labelLang.setObjectName("labelLang")
        self.verticalLayout.addWidget(self.labelLang)
        self.lang = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.lang.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.lang.setObjectName("lang")
        self.verticalLayout.addWidget(self.lang)
        self.spacerLang = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.spacerLang.setMaximumSize(QtCore.QSize(16777215, 10))
        self.spacerLang.setText("")
        self.spacerLang.setObjectName("spacerLang")
        self.verticalLayout.addWidget(self.spacerLang)
        self.labelTranslator = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTranslator.setFont(font)
        self.labelTranslator.setObjectName("labelTranslator")
        self.verticalLayout.addWidget(self.labelTranslator)
        self.translators = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.translators.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.translators.setWordWrap(True)
        self.translators.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.translators.setObjectName("translators")
        self.verticalLayout.addWidget(self.translators)
        self.spacerTransator = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.spacerTransator.setMaximumSize(QtCore.QSize(16777215, 10))
        self.spacerTransator.setText("")
        self.spacerTransator.setObjectName("spacerTransator")
        self.verticalLayout.addWidget(self.spacerTransator)
        self.labelFile = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelFile.setFont(font)
        self.labelFile.setObjectName("labelFile")
        self.verticalLayout.addWidget(self.labelFile)
        self.file = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.file.setWordWrap(True)
        self.file.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.file.setObjectName("file")
        self.verticalLayout.addWidget(self.file)
        self.spacerFile = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spacerFile.sizePolicy().hasHeightForWidth())
        self.spacerFile.setSizePolicy(sizePolicy)
        self.spacerFile.setMaximumSize(QtCore.QSize(16777215, 10))
        self.spacerFile.setText("")
        self.spacerFile.setObjectName("spacerFile")
        self.verticalLayout.addWidget(self.spacerFile)
        self.labelDescription = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelDescription.setFont(font)
        self.labelDescription.setObjectName("labelDescription")
        self.verticalLayout.addWidget(self.labelDescription)
        self.description = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.description.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.description.setObjectName("description")
        self.verticalLayout.addWidget(self.description)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(BookInfoPanel)
        QtCore.QMetaObject.connectSlotsByName(BookInfoPanel)

    def retranslateUi(self, BookInfoPanel):
        _translate = QtCore.QCoreApplication.translate
        BookInfoPanel.setWindowTitle(_translate("BookInfoPanel", "Form"))
        self.title.setText(_translate("BookInfoPanel", "Book title"))
        self.series.setText(_translate("BookInfoPanel", "Book series"))
        self.author.setText(_translate("BookInfoPanel", "Book author"))
        self.cover.setText(_translate("BookInfoPanel", "Book cover"))
        self.labelTags.setText(_translate("BookInfoPanel", "TAGS"))
        self.tags.setText(_translate("BookInfoPanel", "Book tags"))
        self.labelLang.setText(_translate("BookInfoPanel", "LANG"))
        self.lang.setText(_translate("BookInfoPanel", "Book lang"))
        self.labelTranslator.setText(_translate("BookInfoPanel", "TRANSLATOR"))
        self.translators.setText(_translate("BookInfoPanel", "Book translators"))
        self.labelFile.setText(_translate("BookInfoPanel", "FILE"))
        self.file.setText(_translate("BookInfoPanel", "Book file"))
        self.labelDescription.setText(_translate("BookInfoPanel", "DESCRIPTION"))
        self.description.setText(_translate("BookInfoPanel", "Book description"))
from . import resources_rc
