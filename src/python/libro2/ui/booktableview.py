from PyQt5.QtWidgets import QTableView, QAbstractItemView
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtGui import QFontMetrics, QPalette, QColor
from PyQt5.QtSql import QSqlTableModel

import database

class BookTableView(QTableView):
    def __init__(self, parent):
        super(BookTableView, self).__init__(parent)

        font = self.font()
        fm = QFontMetrics(font)
        self.verticalHeader().setDefaultSectionSize(fm.height() + 8)

        palette = self.palette()
        palette.setColor(QPalette.Inactive, QPalette.Highlight, palette.color(QPalette.Active, QPalette.Midlight))
        self.setPalette(palette)
        
        self.setWordWrap(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setHighlightSections(False)
        self.verticalHeader().hide()

        self.setSortingEnabled(True)

        model = BookTableModel(db=database.db)
        model.setTable('book_v')
        model.setSort(1, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicator(1, Qt.AscendingOrder)
        
        model.select()

        model.setHeaderData(0, Qt.Horizontal, 'Id')
        model.setHeaderData(1, Qt.Horizontal, 'Title')
        model.setHeaderData(2, Qt.Horizontal, 'Author')
        model.setHeaderData(3, Qt.Horizontal, 'Series')
        model.setHeaderData(4, Qt.Horizontal, 'Number')
        model.setHeaderData(5, Qt.Horizontal, 'Tags')
        model.setHeaderData(6, Qt.Horizontal, 'Lang')
        model.setHeaderData(7, Qt.Horizontal, 'Translator')
        model.setHeaderData(8, Qt.Horizontal, 'Type')
        model.setHeaderData(9, Qt.Horizontal, 'File')

        self.setModel(model)
        self.hideColumn(0)

    
    def getSelectedId(self):
        list_id = []
        for row in self.selectionModel().selectedRows():
            list_id.append(self.model().record(row.row()).field('id').value())
        return list_id

    def remove(self, list_id):
        database.delete_books(list_id)
        self.updateRows()

    def updateRows(self):

        selectedInexes = []
        currentIndex = self.currentIndex().row()
        for row in self.selectionModel().selectedRows():
            selectedInexes.append(row.row())
        
        self.model().select()
        
        if self.model().rowCount() == 0:
            currentIndex = 0
        elif currentIndex >= self.model().rowCount():
            currentIndex = self.model().rowCount() - 1

        self.setCurrentIndex(self.model().index(currentIndex, 0))
        
        for index in selectedInexes:
            row = self.model().index(index, 0)
            self.selectionModel().select(row, QItemSelectionModel.Rows | QItemSelectionModel.Select)

    def setFilter(self, filter):
        if len(filter) > 0:
            if not (filter.find(':') > -1 or filter.find(' AND ') > -1 or filter.find(' OR ') > -1):
                filter += '*'  
            criteria = 'id in (select rowid FROM book_idx WHERE book_idx MATCH "{}")'.format(filter)
        else:
            criteria = ''

        self.model().setFilter(criteria)
        self.model().select()


class BookTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=None):
        super(BookTableModel, self).__init__(parent, db)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

    def data(self, index, role):
        if role == Qt.ToolTipRole:
            return super(BookTableModel, self).data(index, Qt.DisplayRole)
        
        return super(BookTableModel, self).data(index, role)