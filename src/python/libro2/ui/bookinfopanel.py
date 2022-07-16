import os
import sys

from lxml import etree

from PyQt5.QtWidgets import QWidget, QMenu, QFileDialog, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QPoint, QByteArray, QBuffer, QLocale, pyqtSignal, QCoreApplication

import ebookmeta
from .bookinfopanel_ui import Ui_BookInfoPanel

_t = QCoreApplication.translate

class BookInfoPanel(QWidget, Ui_BookInfoPanel):
    dataChanged = pyqtSignal(bool)

    @property
    def mainInfoCollapsed(self):
        return not self.widgetMain.isVisible()

    @property
    def publishInfoCollapsed(self):
        return not self.widgetPublishInfo.isVisible()
    
    @property
    def coverInfoCollapsed(self):
        return not self.widgetCoverInfo.isVisible()

    @property
    def descriptionInfoCollapsed(self):
        return not self.widgetDescriptionInfo.isVisible()

    @mainInfoCollapsed.setter
    def mainInfoCollapsed(self, value):
        if value:
            self.widgetMain.setVisible(False)
            self.toggleMainInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetMain.setVisible(True)
            self.toggleMainInfo.setIcon(QIcon(':/icons/expanded_12px.png'))


    @publishInfoCollapsed.setter
    def publishInfoCollapsed(self, value):
        if value:
            self.widgetPublishInfo.setVisible(False)
            self.togglePublishInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetPublishInfo.setVisible(True)
            self.togglePublishInfo.setIcon(QIcon(':/icons/expanded_12px.png'))        
    
    @coverInfoCollapsed.setter
    def coverInfoCollapsed(self, value):
        if value:
            self.widgetCoverInfo.setVisible(False)
            self.toggleCoverInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetCoverInfo.setVisible(True)
            self.toggleCoverInfo.setIcon(QIcon(':/icons/expanded_12px.png'))

    @descriptionInfoCollapsed.setter
    def descriptionInfoCollapsed(self, value):
        if value:
            self.widgetDescriptionInfo.setVisible(False)
            self.toggleDescription.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetDescriptionInfo.setVisible(True)
            self.toggleDescription.setIcon(QIcon(':/icons/expanded_12px.png'))       

    def __init__(self, parent):
        super(BookInfoPanel, self).__init__(parent)
        self.setupUi(self)
        self.resizeEvent = self.onResize
        self.cover = None
        self.cover_media_type = None
        self.cover_file_name = None
        self.isDataChanged = False
        self.dataChanged.emit(self.isDataChanged)
        self.bookInfoList = []

        self.customTagLineEdit = QLineEdit()
        self.addTagAction = self.customTagLineEdit.addAction(QIcon(':/icons/more_20px.png'), QLineEdit.TrailingPosition)
        self.addTagAction.setToolTip(_t('info', 'Add fb2 genre'))
        self.addTagAction.triggered.connect(self.onAddTagActionClick)
        self.textTag.setLineEdit(self.customTagLineEdit)

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
        self.textPublishTitle.editTextChanged.connect(self.textChanged)
        self.textPublishTitle.currentIndexChanged.connect(self.textChanged)
        self.textPublishPublisher.editTextChanged.connect(self.textChanged)
        self.textPublishPublisher.currentIndexChanged.connect(self.textChanged)
        self.textPublishCity.editTextChanged.connect(self.textChanged)
        self.textPublishCity.currentIndexChanged.connect(self.textChanged)
        self.textPublishYear.editTextChanged.connect(self.textChanged)
        self.textPublishYear.currentIndexChanged.connect(self.textChanged)
        self.textPublishISBN.editTextChanged.connect(self.textChanged)
        self.textPublishISBN.currentIndexChanged.connect(self.textChanged)
        self.textPublishSeries.editTextChanged.connect(self.textChanged)
        self.textPublishSeries.currentIndexChanged.connect(self.textChanged)
        self.textPublishSeriesIndex.editTextChanged.connect(self.textChanged)
        self.textPublishSeriesIndex.currentIndexChanged.connect(self.textChanged)

        self.labelCoverImage.setContextMenuPolicy(Qt.CustomContextMenu)
        self.labelCoverImage.customContextMenuRequested[QPoint].connect(self.coverContextMenu)

        self.setPlatformUI()

        head_style = 'QToolButton {border: 0px; padding: 2px; color: #1E395B; }' # #1e395b
        self.toggleCoverInfo.setStyleSheet(head_style)
        self.toggleMainInfo.setStyleSheet(head_style)
        self.togglePublishInfo.setStyleSheet(head_style)
        self.toggleDescription.setStyleSheet(head_style)
        
    def coverContextMenu(self, point):
        menu = QMenu()
        actionLoad = menu.addAction(_t('info', 'Load from file...'))
        actionSave = menu.addAction(_t('info', 'Save to file...'))
       
        action = menu.exec_(self.labelCoverImage.mapToGlobal(point))
        
        if action == actionLoad:
            (filename, _) = QFileDialog.getOpenFileName(self, 
                                                        caption=_t('info', 'Load cover from file'), 
                                                        filter=_t('info', 'Image file (*.jpg *.jpeg *.png)'))
            if filename:
                self.loadCoverFromFile(filename)
                self.isDataChanged = True
                self.dataChanged.emit(self.isDataChanged)

        elif action == actionSave:
            (filename, _) = QFileDialog.getSaveFileName(self, 
                                                        caption=_t('info', 'Save cover to file'), 
                                                        directory='cover.jpg', 
                                                        filter=_t('info', 'Image file (*.jpg)'))
            if filename:
                self.saveCoverToFile(filename)
         
    def clearCover(self):
        self.cover = None
        self.labelCoverImage.setText(_t('info', 'No cover image'))
        self.labelImageInfo.setText('')

    def clear(self):
        self.textTitle.clear()
        self.textAuthor.clear()
        self.textSeries.clear()
        self.textNumber.clear()
        self.textTag.clear()
        self.textLang.clear()
        self.textTranslator.clear()
        self.textPublishTitle.clear()
        self.textPublishPublisher.clear()
        self.textPublishCity.clear()
        self.textPublishYear.clear()
        self.textPublishISBN.clear()
        self.textPublishSeries.clear()
        self.textPublishSeriesIndex.clear()

        self.clearCover()
        self.labelCoverImage.setEnabled(False)

        self.textTitle.setEnabled(False)
        self.textAuthor.setEnabled(False)
        self.textSeries.setEnabled(False)
        self.textNumber.setEnabled(False)
        self.textTag.setEnabled(False)
        self.textLang.setEnabled(False)
        self.textTranslator.setEnabled(False)
        self.textPublishTitle.setEnabled(False)
        self.textPublishPublisher.setEnabled(False)
        self.textPublishCity.setEnabled(False)
        self.textPublishYear.setEnabled(False)
        self.textPublishISBN.setEnabled(False)
        self.textPublishSeries.setEnabled(False)
        self.textPublishSeriesIndex.setEnabled(False)

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
        self.textPublishTitle.init()
        self.textPublishPublisher.init()
        self.textPublishCity.init()
        self.textPublishYear.init()
        self.textPublishISBN.init()
        self.textPublishSeries.init()
        self.textPublishSeriesIndex.init()
        

        for book_info in book_info_list:
            self.textTitle.addUserItem(book_info.title)
            self.textAuthor.addUserItem(book_info.authors)
            self.textSeries.addUserItem(book_info.series)
            self.textNumber.addUserItem(str(book_info.series_index))
            self.textTag.addUserItem(book_info.tags)
            self.textLang.addUserItem(book_info.lang)
            self.textTranslator.addUserItem(book_info.translators)
            self.textPublishTitle.addUserItem(book_info.publish_title)
            self.textPublishPublisher.addUserItem(book_info.publish_publisher)
            self.textPublishCity.addUserItem(book_info.publish_city)
            self.textPublishYear.addUserItem(book_info.publish_year)
            self.textPublishISBN.addUserItem(book_info.publish_isbn)
            self.textPublishSeries.addUserItem(book_info.publish_series)
            self.textPublishSeriesIndex.addUserItem(str(book_info.publish_series_index))
       
        self.textTitle.setInitialIndex()
        self.textAuthor.setInitialIndex()
        self.textSeries.setInitialIndex()
        self.textNumber.setInitialIndex()
        self.textTag.setInitialIndex()
        self.textLang.setInitialIndex()
        self.textTranslator.setInitialIndex()
        self.textPublishTitle.setInitialIndex()
        self.textPublishPublisher.setInitialIndex()
        self.textPublishCity.setInitialIndex()
        self.textPublishYear.setInitialIndex()
        self.textPublishISBN.setInitialIndex()
        self.textPublishSeries.setInitialIndex()
        self.textPublishSeriesIndex.setInitialIndex()

        self.textTitle.lineEdit().setCursorPosition(0)
        self.textAuthor.lineEdit().setCursorPosition(0)
        self.textSeries.lineEdit().setCursorPosition(0)
        self.textTag.lineEdit().setCursorPosition(0)
        self.textTranslator.lineEdit().setCursorPosition(0)
        self.textPublishTitle.lineEdit().setCursorPosition(0)
        self.textPublishPublisher.lineEdit().setCursorPosition(0)
        self.textPublishCity.lineEdit().setCursorPosition(0)
        self.textPublishYear.lineEdit().setCursorPosition(0)
        self.textPublishISBN.lineEdit().setCursorPosition(0)
        self.textPublishSeries.lineEdit().setCursorPosition(0)
        self.textPublishSeriesIndex.lineEdit().setCursorPosition(0)

        self.textTitle.setEnabled(True)
        self.textAuthor.setEnabled(True)
        self.textSeries.setEnabled(True)
        self.textNumber.setEnabled(True)
        self.textTag.setEnabled(True)
        self.textLang.setEnabled(True)
        self.textTranslator.setEnabled(True)
        self.textPublishTitle.setEnabled(True)
        self.textPublishPublisher.setEnabled(True)
        self.textPublishCity.setEnabled(True)
        self.textPublishYear.setEnabled(True)
        self.textPublishISBN.setEnabled(True)
        self.textPublishSeries.setEnabled(True)
        self.textPublishSeriesIndex.setEnabled(True)

        if len(book_info_list) == 1:
            self.cover = book_info_list[0].cover_image
            self.cover_media_type = book_info_list[0].cover_media_type
            self.cover_file_name = book_info_list[0].cover_file_name
            self.textDescription.setText(book_info_list[0].description.strip())
            
            self.setCoverImage()
            self.labelCoverImage.setEnabled(True)
        else:
            self.clearCover()
            self.labelCoverImage.setEnabled(False)
            self.textDescription.setText('')

        self.isDataChanged = False
        self.dataChanged.emit(self.isDataChanged)

    def getData(self):
        for bookInfo in self.bookInfoList:
            bookInfo.title = self.textTitle.getUserText(bookInfo.title)
            bookInfo.authors = self.textAuthor.getUserText(bookInfo.authors)
            bookInfo.series = self.textSeries.getUserText(bookInfo.series)
            try:
                bookInfo.series_index = int(self.textNumber.getUserText(bookInfo.series_index))
            except:
                bookInfo.series_index = None
            bookInfo.tags = self.textTag.getUserText(bookInfo.tags)
            bookInfo.lang = self.textLang.getUserText(bookInfo.lang)
            bookInfo.translators = self.textTranslator.getUserText(bookInfo.translators)
            bookInfo.publish_title = self.textPublishTitle.getUserText(bookInfo.publish_title)
            bookInfo.publish_publisher = self.textPublishPublisher.getUserText(bookInfo.publish_publisher)
            bookInfo.publish_city = self.textPublishCity.getUserText(bookInfo.publish_city)
            bookInfo.publish_year = self.textPublishYear.getUserText(bookInfo.publish_year)
            bookInfo.publish_isbn = self.textPublishISBN.getUserText(bookInfo.publish_isbn)
            bookInfo.publish_series = self.textPublishSeries.getUserText(bookInfo.publish_series)
            bookInfo.publish_series_index = self.textPublishSeriesIndex.getUserText(bookInfo.publish_series_index)

        if len(self.bookInfoList) == 1:
            self.bookInfoList[0].cover_image = self.cover
            self.bookInfoList[0].cover_media_type = self.cover_media_type
            self.bookInfoList[0].cover_file_name = self.cover_file_name

        return self.bookInfoList


    def setCoverImage(self):
        if self.cover:
            pix = QPixmap()
            pix.loadFromData(self.cover)
            scaled_pix = pix.scaled(self.labelCoverImage.width() - 4, self.labelCoverImage.height() - 4, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.labelCoverImage.setPixmap(scaled_pix)

            cover_data_size = '{0} KB'.format(int(len(self.cover) / 1024))
            cover_size = '{0}x{1}'.format(pix.size().width(), pix.size().height())
            self.labelImageInfo.setText(self.cover_media_type + '\n' +cover_size + '\n' + cover_data_size)

    def loadCoverFromFile(self, filename):
        image_format = None
        
        if not self.cover_media_type:
            # Book without cover - new filename
            self.cover_media_type = 'image/jpeg'
            self.cover_file_name = 'cover.jpg'
        
        if self.cover_media_type == 'image/jpeg':
            image_format = 'JPG'
        elif self.cover_media_type == 'image/png':
            image_format = 'PNG'

        if os.path.exists(filename):
            pixmap = QPixmap()
            if pixmap.load(filename):
                data = QByteArray()
                buff = QBuffer(data)
                pixmap.save(buff, image_format)
                self.cover = bytes(buff.buffer())
                self.setCoverImage()

    def saveCoverToFile(self, filename):
        if not filename.lower().endswith('.jpg'):
            filename += '.jpg'

        pixmap = QPixmap()
        pixmap.loadFromData(self.cover)
        pixmap.save(filename, 'JPG')

    def onResize(self, event):
        width = int(round(self.width() * 0.55))
        height = int(round(width * 1.54, 0))
        
        self.labelCoverImage.setMinimumSize(width, height)
        self.labelCoverImage.setMaximumSize(width, height)
       
        self.setCoverImage()
        

    def onAddTagActionClick(self):
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

        action = menu.exec_(self.customTagLineEdit.mapToGlobal(QPoint(self.customTagLineEdit.width(), 0)))
        if action:
            text = self.textTag.currentText()
            if text in (self.textTag.Blank, self.textTag.Keep):
                text = action.data()
            else:
                tags = [x.strip() for x in text.split(',')]
                if action.data() not in tags:
                    tags.append(action.data())
                    text = ', '.join(tags)
                    
            self.textTag.setCurrentText(text)


    def setPlatformUI(self):
        if sys.platform == 'win32':
            font = QFont('Segoe UI', 9)
            font_bold = QFont('Segoe UI', 9)
            self.label.setFont(font)
            self.label_2.setFont(font)
            self.label_3.setFont(font)
            self.label_4.setFont(font)
            self.label_8.setFont(font)
            self.label_6.setFont(font)
            self.label_7.setFont(font)
            self.labelImageInfo.setFont(font)
            self.textTitle.setFont(font)
            self.textTitle.lineEdit().setFont(font)
            self.textAuthor.setFont(font)
            self.textAuthor.lineEdit().setFont(font)
            self.textSeries.setFont(font)
            self.textSeries.lineEdit().setFont(font)
            self.textNumber.setFont(font)
            self.textNumber.lineEdit().setFont(font)
            self.textTag.setFont(font)
            self.textTag.lineEdit().setFont(font)
            self.textLang.setFont(font)
            self.textLang.lineEdit().setFont(font)
            self.textTranslator.setFont(font)
            self.textTranslator.lineEdit().setFont(font)
            self.toggleMainInfo.setFont(font_bold)
            self.togglePublishInfo.setFont(font_bold)
            self.toggleCoverInfo.setFont(font_bold)
            self.label_5.setFont(font)
            self.label_9.setFont(font)
            self.label_10.setFont(font)
            self.label_11.setFont(font)
            self.label_12.setFont(font)
            self.label_15.setFont(font)
            self.label_14.setFont(font)
            self.textPublishTitle.setFont(font)
            self.textPublishTitle.lineEdit().setFont(font)
            self.textPublishPublisher.setFont(font)
            self.textPublishPublisher.lineEdit().setFont(font)
            self.textPublishCity.setFont(font)
            self.textPublishCity.lineEdit().setFont(font)
            self.textPublishYear.setFont(font)
            self.textPublishYear.lineEdit().setFont(font)
            self.textPublishISBN.setFont(font)
            self.textPublishISBN.lineEdit().setFont(font)
            self.textPublishSeries.setFont(font)
            self.textPublishSeries.lineEdit().setFont(font)
            self.textPublishSeriesIndex.setFont(font)
            self.textPublishSeriesIndex.lineEdit().setFont(font)

            self.toggleDescription.setFont(font_bold)
            self.textDescription.setFont(font)
        elif sys.platform == 'darwin':
            font = self.toggleMainInfo.font()
            font.setPointSize(12)
            self.toggleMainInfo.setFont(font)
            self.togglePublishInfo.setFont(font)
            self.toggleCoverInfo.setFont(font)
            self.toggleDescription.setFont(font)
        else:
            pass


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

    def onMainInfoToggle(self):
        if self.widgetMain.isVisible():
            self.widgetMain.setVisible(False)
            self.toggleMainInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetMain.setVisible(True)
            self.toggleMainInfo.setIcon(QIcon(':/icons/expanded_12px.png'))

    def onPublishInfoToggle(self):
        if self.widgetPublishInfo.isVisible():
            self.widgetPublishInfo.setVisible(False)
            self.togglePublishInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetPublishInfo.setVisible(True)
            self.togglePublishInfo.setIcon(QIcon(':/icons/expanded_12px.png'))
            
    def onCoverInfoToggle(self):
        if self.widgetCoverInfo.isVisible():
            self.widgetCoverInfo.setVisible(False)
            self.toggleCoverInfo.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetCoverInfo.setVisible(True)
            self.toggleCoverInfo.setIcon(QIcon(':/icons/expanded_12px.png'))


    def onDescriptionInfoToggle(self):
        if self.widgetDescriptionInfo.isVisible():
            self.widgetDescriptionInfo.setVisible(False)
            self.toggleDescription.setIcon(QIcon(':/icons/collapsed_12px.png'))
        else:
            self.widgetDescriptionInfo.setVisible(True)
            self.toggleDescription.setIcon(QIcon(':/icons/expanded_12px.png'))