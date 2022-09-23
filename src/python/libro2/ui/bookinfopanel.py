import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QCoreApplication

from .bookinfopanel_ui import Ui_BookInfoPanel
import config

settings = config.settings

_t = QCoreApplication.translate

class BookInfoPanel(QWidget, Ui_BookInfoPanel):
    def __init__(self, parent):
        super(BookInfoPanel, self).__init__(parent)
        self.setupUi(self)
        self.setPlatformUI()
        self.clear()
        self._book_info_list = []
 
    def clear(self):
        self.title.clear()
        self.author.clear()
        self.series.clear()
        self.cover.clear()
        self.coverInfo.clear()
        self.tags.clear()
        self.lang.clear()
        self.translators.clear()
        self.description.clear()

        self.labelAuthor.setVisible(False)
        self.labelSeries.setVisible(False)
        self.labelTags.setVisible(False)
        self.labelLang.setVisible(False)
        self.labelTranslator.setVisible(False)
        self.labelDescription.setVisible(False)

        self.cover.setVisible(False)
        self.coverInfo.setVisible(False)
        self.title.setText(_t('info', 'No items'))
        self.author.setVisible(False)
        self.series.setVisible(False)
        self.tags.setVisible(False)
        self.lang.setVisible(False)
        self.translators.setVisible(False)
        self.description.setVisible(False)

    def setData(self, book_info_list):
        self._book_info_list = book_info_list
        self.displayData()

    def displayData(self):
        self.clear()

        if len(self._book_info_list) == 1:
            book_info = self._book_info_list[0]
            self.title.setText(book_info.title)

            if book_info.authors:
                self.labelAuthor.setVisible(True)
                self.author.setVisible(True)
                self.author.setText(book_info.authors)
            
            if book_info.series:
                self.labelSeries.setVisible(True)
                self.series.setVisible(True)
                if book_info.series_index:
                    self.series.setText(f'{book_info.series} ({book_info.series_index})')
                else:
                    self.series.setText(f'{book_info.series}')    

            if book_info.tags_description:
                self.labelTags.setVisible(True)
                self.tags.setVisible(True)
                self.tags.setText(book_info.tags_description)

            if book_info.lang:
                self.labelLang.setVisible(True)
                self.lang.setVisible(True)
                self.lang.setText(book_info.lang)

            if book_info.translators:
                self.labelTranslator.setVisible(True)
                self.translators.setVisible(True)
                self.translators.setText(book_info.translators)
       
            if book_info.description:
                self.labelDescription.setVisible(True)
                self.description.setVisible(True)
                self.description.setText(book_info.description.strip())
       
            if book_info.cover_image:
                self.cover.setVisible(True)
                self.coverInfo.setVisible(True)
                pix = QPixmap()
                pix.loadFromData(book_info.cover_image)
                
                scale_width = int(settings.ui_cover_image_width * self.scale_factor())
                scale_height = int(scale_width * pix.height() / pix.width())
                scaled_pix = pix.scaled(scale_width, scale_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover.setPixmap(scaled_pix)

                cover_type = book_info.cover_media_type
                cover_width = pix.width()
                cover_height = pix.height()
                cover_size = int(len(book_info.cover_image) / 1024)
                self.coverInfo.setText(f'{cover_type}\n{cover_width}x{cover_height}\n{cover_size} KB')

          
        elif len(self._book_info_list) > 1:
            self.title.setText(_t('info', 'Selected items: {0}').format(len(self._book_info_list)))

    def scale_factor(self):
        if sys.platform == 'darwin':
            base_dpi = 72
        else:
            base_dpi = 96

        return self.screen().logicalDotsPerInchX() / base_dpi

    def setPlatformUI(self):
        if sys.platform == 'darwin':
            font = self.title.font()
            font.setPointSize(18) 
            self.title.setFont(font)

 


 