import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QCoreApplication, QByteArray, QBuffer

import ebookmeta

from .editdialog_ui import Ui_EditDialog

_t = QCoreApplication.translate

class EditDialog(QDialog, Ui_EditDialog):
    def __init__(self, parent, book_info_list):
        super(EditDialog, self).__init__(parent)
        self.setupUi(self)

        self.book_info_list = book_info_list

        self.setChecked(False, self.checkTitle, self.textTitle)
        self.setChecked(False, self.checkAuthor, self.textAuthor)
        self.setChecked(False, self.checkSeries, self.textSeries)
        self.setChecked(False, self.checkSeriesIndex, self.textSeriesIndex)
        self.setChecked(False, self.checkTags, self.textTags)
        self.setChecked(False, self.checkLang, self.textLang)
        self.setChecked(False, self.checkTranslator, self.textTranslator)

        self.setChecked(False, self.checkPublishTitle, self.textPublishTitle)
        self.setChecked(False, self.checkPublishPublisher, self.textPublishPublisher)
        self.setChecked(False, self.checkPublishCity, self.textPublishCity)
        self.setChecked(False, self.checkPublishYear, self.textPublishYear)
        self.setChecked(False, self.checkPublishISBN, self.textPublishISBN)
        self.setChecked(False, self.checkPublishSeries, self.textPublishSeries)
        self.setChecked(False, self.checkPublishSeriesIndex, self.textPublishSeriesIndex)

        self.btnLoadFromFile.setEnabled(False)
        self.btnSaveToFile.setEnabled(False)

        self.checkTitle.clicked.connect(lambda x: self.onCheckClicked(x, self.textTitle))
        self.checkAuthor.clicked.connect(lambda x: self.onCheckClicked(x, self.textAuthor))
        self.checkSeries.clicked.connect(lambda x: self.onCheckClicked(x, self.textSeries))
        self.checkSeriesIndex.clicked.connect(lambda x: self.onCheckClicked(x, self.textSeriesIndex))
        self.checkTags.clicked.connect(lambda x: self.onCheckClicked(x, self.textTags))
        self.checkLang.clicked.connect(lambda x: self.onCheckClicked(x, self.textLang))
        self.checkTranslator.clicked.connect(lambda x: self.onCheckClicked(x, self.textTranslator))

        self.checkPublishTitle.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishTitle))
        self.checkPublishPublisher.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishPublisher))
        self.checkPublishCity.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishCity))
        self.checkPublishYear.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishYear))
        self.checkPublishISBN.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishISBN))
        self.checkPublishSeries.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishSeries))
        self.checkPublishSeriesIndex.clicked.connect(lambda x: self.onCheckClicked(x, self.textPublishSeriesIndex))

        self.setData()
        
    def setData(self):
        title = set()
        author = set()
        series = set()
        series_index = set()
        tags = set()
        lang = set()
        tranlator = set()

        publishTitle = set()
        publishPublisher = set()
        publishCity = set()
        publishYear = set()
        publishISBN = set()
        publishSeries = set()
        publishSeriesIndex = set()

        for book in self.book_info_list:
            title.add(book.title)
            author.add(book.authors)
            series.add(book.series)
            series_index.add(book.series_index)
            tags.add(book.tags)
            lang.add(book.lang)
            tranlator.add(book.translators)

            publishTitle.add(book.publish_title)
            publishPublisher.add(book.publish_publisher)
            publishCity.add(book.publish_city)
            publishYear.add(book.publish_year)
            publishISBN.add(book.publish_isbn)
            publishSeries.add(book.publish_series)
            publishSeriesIndex.add(book.publish_series_index)

        
        #### Basic info
        if len(title) == 1:
            self.setChecked(True, self.checkTitle, self.textTitle)
            self.textTitle.setText(list(title)[0])
            self.textTitle.setCursorPosition(0)

        if len(author) == 1:
            self.setChecked(True, self.checkAuthor, self.textAuthor)
            self.textAuthor.setText(list(author)[0])
            self.textAuthor.setCursorPosition(0)

        if len(series) == 1:
            self.setChecked(True, self.checkSeries, self.textSeries)
            self.textSeries.setText(list(series)[0])
            self.textSeries.setCursorPosition(0)
        
        if len(series_index) == 1:
            self.setChecked(True, self.checkSeriesIndex, self.textSeriesIndex)
            self.textSeriesIndex.setText(str(list(series_index)[0]))
        
        if len(tags) == 1:
            self.setChecked(True, self.checkTags, self.textTags)
            self.textTags.setText(list(tags)[0])
            self.textTags.setCursorPosition(0)
        
        if len(lang) == 1:
            self.setChecked(True, self.checkLang, self.textLang)
            self.textLang.setText(list(lang)[0])
            self.textLang.setCursorPosition(0)
        
        if len(tranlator) == 1:
            self.setChecked(True, self.checkTranslator, self.textTranslator)
            self.textTranslator.setText(list(tranlator)[0])
            self.textTranslator.setCursorPosition(0)

        ##### Publish info 
        if len(publishTitle) == 1:
            self.setChecked(True, self.checkPublishTitle, self.textPublishTitle)
            self.textPublishTitle.setText(list(publishTitle)[0])
            self.textPublishTitle.setCursorPosition(0)

        if len(publishPublisher) == 1:
            self.setChecked(True, self.checkPublishPublisher, self.textPublishPublisher)
            self.textPublishPublisher.setText(list(publishPublisher)[0])
            self.textPublishPublisher.setCursorPosition(0)

        if len(publishCity) == 1:
            self.setChecked(True, self.checkPublishCity, self.textPublishCity)
            self.textPublishCity.setText(list(publishCity)[0])
            self.textPublishCity.setCursorPosition(0)

        if len(publishYear) == 1:
            self.setChecked(True, self.checkPublishYear, self.textPublishYear)
            self.textPublishYear.setText(list(publishYear)[0])
            self.textPublishYear.setCursorPosition(0)
        
        if len(publishISBN) == 1:
            self.setChecked(True, self.checkPublishISBN, self.textPublishISBN)
            self.textPublishISBN.setText(list(publishISBN)[0])
            self.textPublishISBN.setCursorPosition(0)
        
        if len(publishSeries) == 1:
            self.setChecked(True, self.checkPublishSeries, self.textPublishSeries)
            self.textPublishSeries.setText(list(publishSeries)[0])
            self.textPublishSeries.setCursorPosition(0)
        
        if len(publishSeriesIndex) == 1:
            self.setChecked(True, self.checkPublishSeriesIndex, self.textPublishSeriesIndex)
            self.textPublishSeriesIndex.setText(str(list(publishSeriesIndex)[0]))

        if len(self.book_info_list) == 1:
            self.btnLoadFromFile.setEnabled(True)
            self.btnSaveToFile.setEnabled(True)
            self.setCoverImage()
        else:
            self.cover.setEnabled(False)


        # self.setWindowTitle(_t('edit', 'Edit {0} file(s)'.format(len(self.book_info_list))))

    def getData(self):
        for book in self.book_info_list:
            if self.checkTitle.isChecked():
                book.title = self.textTitle.text()
            
            if self.checkAuthor.isChecked():
                book.authors = self.textAuthor.text()

            if self.checkSeries.isChecked():
                book.series = self.textSeries.text()

            if self.checkSeriesIndex.isChecked():
                try:
                    if self.textSeriesIndex.text():
                        book.series_index = int(self.textSeriesIndex.text())
                    else:
                        book.series_index = None
                except:
                    pass
            
            if self.checkTags.isChecked():
                book.tags = self.textTags.text()

            if self.checkLang.isChecked():
                book.lang = self.textLang.text()

            if self.checkTranslator.isChecked():
                book.translators = self.textTranslator.text()

            if self.checkPublishTitle.isChecked():
                book.publish_title = self.textPublishTitle.text()

            if self.checkPublishPublisher.isChecked():
                book.publish_publisher = self.textPublishPublisher.text()

            if self.checkPublishCity.isChecked():
                book.publish_city = self.textPublishCity.text()

            if self.checkPublishYear.isChecked():
                book.publish_year = self.textPublishYear.text()

            if self.checkPublishISBN.isChecked():
                book.publish_isbn = self.textPublishISBN.text()

            if self.checkPublishSeries.isChecked():
                book.publish_series = self.textPublishSeries.text()

            if self.checkPublishSeriesIndex.isChecked():
                book.publish_series_index = self.textPublishSeriesIndex.text()


        return self.book_info_list

    def setChecked(self, value, checkBox, textEdit):
        checkBox.setChecked(value)
        self.onCheckClicked(checkBox.isChecked(), textEdit)

    def onCheckClicked(self, isChecked, textEdit):
        textEdit.setEnabled(isChecked)
        if not isChecked:
            textEdit.clear()

        if textEdit.objectName() == 'textTags':
            self.btnAddGenre.setEnabled(isChecked)

    def onBtnLoadClick(self):
        (filename, _) = QFileDialog.getOpenFileName(self, 
                                                    caption=_t('edit', 'Load cover from file'), 
                                                    filter=_t('edit', 'Image file (*.jpg *.jpeg *.png)'))
        if filename:
            self.loadCoverFromFile(filename)

    def loadCoverFromFile(self, filename):
        image_format = None

        if not self.book_info_list[0].cover_media_type:
            # Book without cover - new filename
            self.book_info_list[0].cover_media_type = 'image/jpeg'
            self.book_info_list[0].cover_file_name = 'cover.jpg'
        
        if self.book_info_list[0].cover_media_type == 'image/jpeg':
            image_format = 'JPG'
        elif self.book_info_list[0].cover_media_type == 'image/png':
            image_format = 'PNG'

        if os.path.exists(filename):
            pixmap = QPixmap()
            if pixmap.load(filename):
                data = QByteArray()
                buff = QBuffer(data)
                pixmap.save(buff, image_format)
                self.book_info_list[0].cover_image = bytes(buff.buffer())
                self.setCoverImage()


    def setCoverImage(self):
        if self.book_info_list[0].cover_image:
            pix = QPixmap()
            pix.loadFromData(self.book_info_list[0].cover_image)
            scaled_pix = pix.scaled(self.cover.width() - 4, self.cover.height() - 4, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.cover.setPixmap(scaled_pix)


    def onBtnSaveClick(self):
        (filename, _) = QFileDialog.getSaveFileName(self, 
                                                    caption=_t('info', 'Save cover to file'), 
                                                    directory='cover.jpg', 
                                                    filter=_t('info', 'Image file (*.jpg)'))
        if filename:
            if not filename.lower().endswith('.jpg'):
                filename += '.jpg'

            pixmap = QPixmap()
            pixmap.loadFromData(self.book_info_list[0].cover_image)
            pixmap.save(filename, 'JPG')


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

  