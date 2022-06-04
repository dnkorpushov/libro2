import os

from lxml import etree

from PyQt5.QtWidgets import QWidget, QMenu, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QPoint, QByteArray, QBuffer, QLocale, pyqtSignal

import ebookmeta
from .bookinfopanel_ui import Ui_BookInfoPanel
from .comboedit import ComboEditItemAction

class BookInfoPanel(QWidget, Ui_BookInfoPanel):
    dataChanged = pyqtSignal(bool)

    def __init__(self, parent):
        super(BookInfoPanel, self).__init__(parent)
        self.setupUi(self)
        self.resizeEvent = self.onResize
        self.cover = None
        self.isDataChanged = False
        self.dataChanged.emit(self.isDataChanged)
        self.bookInfoList = []

        self.textTitle.editTextChanged.connect(self.textChanged)
        self.textTitle.currentIndexChanged.connect(self.textChanged)
        self.textAuthor.editTextChanged.connect(self.textChanged)
        self.textAuthor.currentIndexChanged.connect(self.textChanged)
        self.textSeries.editTextChanged.connect(self.textChanged)
        self.textSeries.currentIndexChanged.connect(self.textChanged)
        self.textNumber.editTextChanged.connect(self.textChanged)
        self.textNumber.currentIndexChanged.connect(self.textChanged)
        self.textTag.editTextChanged.connect(self.textChanged)
        self.textTag.currentIndexChanged.connect(self.textChanged)
        self.textLang.editTextChanged.connect(self.textChanged)
        self.textLang.currentIndexChanged.connect(self.textChanged)
        self.textTranslator.editTextChanged.connect(self.textChanged)
        self.textTranslator.currentIndexChanged.connect(self.textChanged)

        self.labelCoverImage.setContextMenuPolicy(Qt.CustomContextMenu)
        self.labelCoverImage.customContextMenuRequested[QPoint].connect(self.coverContextMenu)

        self.toolButton.clicked.connect(self.onToolButtonClick)
        
    def coverContextMenu(self, point):
        menu = QMenu()
        actionLoad = menu.addAction('Load from file...')
        actionSave = menu.addAction('Save to file...')
        actionClear = menu.addAction('Clear')

        action = menu.exec_(self.labelCoverImage.mapToGlobal(point))
        
        if action == actionLoad:
            (filename, _) = QFileDialog.getOpenFileName(self, caption='Load cover from file', filter='Image file (*.jpg *.jpeg *.png)')
            if filename:
                self.loadCoverFromFile(filename)
                self.isDataChanged = True
                self.dataChanged.emit(self.isDataChanged)

        elif action == actionSave:
            (filename, _) = QFileDialog.getSaveFileName(self, caption='Save cover to file', directory='cover.jpg', filter='Image file (*.jpg)')
            if filename:
                self.saveCoverToFile(filename)

        elif action == actionClear:
            self.labelCoverImage.clear()
            self.clearCover()
            self.iDataChanged = True
            self.dataChanged.emit(self.isDataChanged)
         
    def clearCover(self):
        self.cover = None
        self.labelCoverImage.setText('No cover image')

    def clear(self):
        self.textTitle.clear()
        self.textAuthor.clear()
        self.textSeries.clear()
        self.textNumber.clear()
        self.textTag.clear()
        self.textLang.clear()
        self.textTranslator.clear()

        self.labelCoverImage.clear()
        self.labelCoverImage.setText('No cover image')
        self.labelCoverImage.setEnabled(False)
        self.labelImageInfo.setText('0x0\n0 KB')

        self.textTitle.setEnabled(False)
        self.textAuthor.setEnabled(False)
        self.textSeries.setEnabled(False)
        self.textNumber.setEnabled(False)
        self.textTag.setEnabled(False)
        self.textLang.setEnabled(False)
        self.textTranslator.setEnabled(False)
        self.toolButton.setEnabled(False)


        self.isDataChanged = False
        self.dataChanged.emit(self.isDataChanged)
        self.bookInfoList = []

    def textChanged(self):
        self.isDataChanged = True
        self.dataChanged.emit(self.isDataChanged)
   
    def setData(self, book_info_list):
        self.bookInfoList = book_info_list

        self.textTitle.init()
        self.textAuthor.init()
        self.textSeries.init()
        self.textNumber.init()
        self.textTag.init()
        self.textLang.init()
        self.textTranslator.init()

        for book_info in book_info_list:
            self.textTitle.addUserItem(book_info['title'])
            self.textAuthor.addUserItem(book_info['author'])
            self.textSeries.addUserItem(book_info['series'])
            self.textNumber.addUserItem(str(book_info['series_index']))
            self.textTag.addUserItem(book_info['tags'])
            self.textLang.addUserItem(book_info['lang'])
            self.textTranslator.addUserItem(book_info['translator'])
       
        self.textTitle.setInitialIndex()
        self.textAuthor.setInitialIndex()
        self.textSeries.setInitialIndex()
        self.textNumber.setInitialIndex()
        self.textTag.setInitialIndex()
        self.textLang.setInitialIndex()
        self.textTranslator.setInitialIndex()

        self.textTitle.lineEdit().setCursorPosition(0)
        self.textAuthor.lineEdit().setCursorPosition(0)
        self.textSeries.lineEdit().setCursorPosition(0)
        self.textTag.lineEdit().setCursorPosition(0)
        self.textTranslator.lineEdit().setCursorPosition(0)

        self.textTitle.setEnabled(True)
        self.textAuthor.setEnabled(True)
        self.textSeries.setEnabled(True)
        self.textNumber.setEnabled(True)
        self.textTag.setEnabled(True)
        self.textLang.setEnabled(True)
        self.textTranslator.setEnabled(True)
        self.toolButton.setEnabled(True)

        if len(book_info_list) == 1:
            self.cover = book_info_list[0]['cover_image']
            self.setCoverImage()
            self.labelCoverImage.setEnabled(True)
        else:
            self.cover = None
            self.labelCoverImage.setText('No cover image')
            self.labelCoverImage.setEnabled(False)

        self.isDataChanged = False
        self.dataChanged.emit(self.isDataChanged)

    
    def getData(self):

        for bookInfo in self.bookInfoList:
            bookInfo['title'] = self.textTitle.getUserText(bookInfo['title'])
            bookInfo['author'] = self.textAuthor.getUserText(bookInfo['author'])
            bookInfo['series'] = self.textSeries.getUserText(bookInfo['series'])
            try:
                bookInfo['series_index'] = int(self.textNumber.getUserText(bookInfo['series_index']))
            except:
                bookInfo['series_index'] = None
            bookInfo['tags'] = self.textTag.getUserText(bookInfo['tags'])
            bookInfo['lang'] = self.textLang.getUserText(bookInfo['lang'])
            bookInfo['translator'] = self.textTranslator.getUserText(bookInfo['translator'])
            
            
        if len(self.bookInfoList) == 1:
            self.bookInfoList[0]['cover_image'] = self.cover

        return self.bookInfoList


    def setCoverImage(self):
        if self.cover:
            pix = QPixmap()
            pix.loadFromData(self.cover)
            scaled_pix = pix.scaled(self.labelCoverImage.width() - 4, self.labelCoverImage.height() - 4, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.labelCoverImage.setPixmap(scaled_pix)

            cover_data_size = '{0} KB'.format(int(len(self.cover) / 1024))
            cover_size = '{0}x{1}'.format(pix.size().width(), pix.size().height())
            self.labelImageInfo.setText(cover_size + '\n' + cover_data_size)

    def loadCoverFromFile(self, filename):
        if os.path.exists(filename):
            pixmap = QPixmap()
            if pixmap.load(filename):
                data = QByteArray()
                buff = QBuffer(data)
                pixmap.save(buff, 'JPG')
                self.cover = bytes(buff.buffer())
                self.setCoverImage()

    def saveCoverToFile(self, filename):
        if not filename.lower().endswith('.jpg'):
            filename += '.jpg'

        pixmap = QPixmap()
        pixmap.loadFromData(self.cover)
        pixmap.save(filename, 'JPG')

    def onResize(self, event):
        self.labelCoverImage.setMinimumSize(self.width() - 160, int((self.width() - 160) * 1.54))
        self.setCoverImage()
        

    def onToolButtonClick(self):
        menuData = self.getGenres(QLocale.system().name()[:2])

        menu = QMenu()
        submenus = []
        for item in menuData:
            submenu = QMenu(item['title'])
            for i in item['submenu']:
                menuAction = submenu.addAction(i['title'])
                menuAction.setData(i['value'])
            submenus.append(submenu)
            menu.addMenu(submenu)

        action = menu.exec_(self.toolButton.mapToGlobal(QPoint(0, 0)))
        if action:
            text = self.textTag.currentText()
            if text in (ComboEditItemAction.Blank, ComboEditItemAction.Keep):
                text = action.data()
            else:
                tags = [x.strip() for x in text.split(',')]
                if action.data() not in tags:
                    tags.append(action.data())
                    text = ', '.join(tags)
                    
            self.textTag.setCurrentText(text)

    def getGenres(self, lang='ru'):
        if lang not in ['ru', 'en']:
            lang = 'en'

        genres = etree.fromstring(ebookmeta.fb2genres.fb2genres, parser=etree.XMLParser())
        genre_menu = []

        for genre in genres:
            genre_value = genre.attrib['value']
            genre_name = ''
            for genre_data in genre:
                subgenre_menu = []
                if genre_data.tag == 'root-descr' and genre_data.attrib['lang'] == lang:
                    genre_name = genre_data.attrib['genre-title']
                elif genre_data.tag == 'subgenres':
                    for subgenre in genre_data:
                        subgenre_value = subgenre.attrib['value']
                        subgenre_name = ''
                        for subgenre_data in subgenre:
                            if subgenre_data.tag == 'genre-descr' and subgenre_data.attrib['lang'] == lang:
                                subgenre_name = subgenre_data.attrib['title']
                        subgenre_menu.append({'value': subgenre_value, 'title': subgenre_name})

            genre_menu.append({'value': genre_value, 'title': genre_name, 'submenu': subgenre_menu})
        return genre_menu
