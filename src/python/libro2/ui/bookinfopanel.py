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
        self.author.clear()
        self.series.clear()
        self.cover.clear()
        self.tags.clear()
        self.lang.clear()
        self.translators.clear()
        self.description.clear()

        self.labelTitle.setVisible(False)
        self.labelAuthor.setVisible(False)
        self.labelSeries.setVisible(False)
        self.labelTags.setVisible(False)
        self.labelLang.setVisible(False)
        self.labelTranslator.setVisible(False)
        self.labelDescription.setVisible(False)

        self.cover.setVisible(False)
        self.title.setText(_t('info', 'No items'))
        self.author.setVisible(False)
        self.series.setVisible(False)
        self.tags.setVisible(False)
        self.lang.setVisible(False)
        self.translators.setVisible(False)
        self.description.setVisible(False)

    def setData(self, book_info_list):
        self.clear()

        if len(book_info_list) == 1:
            book_info = book_info_list[0]
            self.labelTitle.setVisible(True)
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
                pix = QPixmap()
                pix.loadFromData(book_info.cover_image)
                scaled_pix = pix.scaled(130, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.cover.setPixmap(scaled_pix)
          
        elif len(book_info_list) > 1:
            self.title.setText(_t('info', 'Selected items: {0}').format(len(book_info_list)))
       

    def setPlatformUI(self):
        pass
        # if sys.platform == 'darwin':
        #     font = self.title.font()
        #     font.setPointSize(18) 
        #     self.title.setFont(font)

 


 