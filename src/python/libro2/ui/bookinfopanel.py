import sys

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QCoreApplication

from .bookinfopanel_ui import Ui_BookInfoPanel

_t = QCoreApplication.translate

class BookInfoPanel(QWidget, Ui_BookInfoPanel):
    def __init__(self, parent):
        super(BookInfoPanel, self).__init__(parent)
        self.setupUi(self)
        self.setPlatformUI()
        self.clear()
 
    def clear(self):
        self.title.clear()
        self.series.clear()
        self.author.clear()
        self.cover.clear()
        self.tags.clear()
        self.lang.clear()
        self.translators.clear()
        self.file.clear()
        self.description.clear()

        self.labelTags.setVisible(False)
        self.labelLang.setVisible(False)
        self.labelTranslator.setVisible(False)
        self.labelFile.setVisible(False)
        self.labelDescription.setVisible(False)

        self.spacerLang.setVisible(False)
        self.spacerTags.setVisible(False)
        self.spacerTransator.setVisible(False)
        self.spacerFile.setVisible(False)

        self.title.setText(_t('info', 'No items'))
        self.author.setVisible(False)
        self.series.setVisible(False)
        self.tags.setVisible(False)
        self.lang.setVisible(False)
        self.translators.setVisible(False)
        self.file.setVisible(False)
        self.description.setVisible(False)

    def setData(self, book_info_list):
        self.clear()

        if len(book_info_list) == 1:
            book_info = book_info_list[0]
            self.title.setText(book_info.title)

            if book_info.authors:
                self.author.setVisible(True)
                self.author.setText(book_info.authors)
            
            if book_info.series:
                self.series.setVisible(True)
                if book_info.series_index:
                    self.series.setText(f'{book_info.series} ({book_info.series_index})')
                else:
                    self.series.setText(f'{book_info.series}')    

            if book_info.tags_description:
                self.labelTags.setVisible(True)
                self.tags.setVisible(True)
                self.spacerTags.setVisible(True)
                self.tags.setText(book_info.tags_description)

            if book_info.lang:
                self.labelLang.setVisible(True)
                self.lang.setVisible(True)
                self.spacerLang.setVisible(True)
                self.lang.setText(book_info.lang)

            if book_info.translators:
                self.labelTranslator.setVisible(True)
                self.translators.setVisible(True)
                self.spacerTransator.setVisible(True)
                self.translators.setText(book_info.translators)
       
            if book_info.file:
                self.labelFile.setVisible(True)
                self.file.setVisible(True)
                self.spacerFile.setVisible(True)
                self.file.setText(book_info.file)

            if book_info.description:
                self.labelDescription.setVisible(True)
                self.description.setVisible(True)
                self.description.setText(book_info.description.strip())
       
            if book_info.cover_image:
                self.cover.setVisible(True)
                pix = QPixmap()
                pix.loadFromData(book_info.cover_image)
                scaled_pix = pix.scaled(130, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover.setPixmap(scaled_pix)
          
        elif len(book_info_list) > 1:
            self.title.setText(_t('info', 'Selected items: {0}').format(len(book_info_list)))
       

    def setPlatformUI(self):

        if sys.platform == 'win32':
            font = QFont('Segoe UI', 9)
            font_bold = QFont('Segoe UI', 9, weight=700)
            font_caption = QFont('Segoe UI', 14)
        else:
            font = self.title.font()
            font_caption = self.title.font()
            font_caption.setPointSize(14)
            font_bold = self.title.font()
            font_bold.setBold(True)

        self.labelTags.setFont(font_bold)
        self.labelLang.setFont(font_bold)
        self.labelTranslator.setFont(font_bold)
        self.labelDescription.setFont(font_bold)

        self.title.setFont(font_caption)
        self.author.setFont(font)

        self.series.setFont(font_bold)

        self.tags.setFont(font)
        self.lang.setFont(font)
        self.translators.setFont(font)
        self.description.setFont(font)



 