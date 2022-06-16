import sys
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QMenu, QAction, QApplication
from PyQt5.QtCore import Qt, QItemSelectionModel, QCoreApplication
from PyQt5.QtGui import QFontMetrics, QPalette
from PyQt5.QtSql import QSqlTableModel

import database

_t = QCoreApplication.translate

class BookTableView(QTableView):
    def __init__(self, parent):
        super(BookTableView, self).__init__(parent)

        font = self.font()
        fm = QFontMetrics(font)
        self.verticalHeader().setDefaultSectionSize(fm.height() + 8)

        # OS UI Hacks
        if sys.platform == 'win32':
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
        model.setTable('books_v')
        model.setSort(1, Qt.AscendingOrder)
        self.horizontalHeader().setSortIndicator(1, Qt.AscendingOrder)
        
        model.select()

        self.headers = [
            'Id', 
            _t('table','Title'), 
            _t('table','Author'), 
            _t('table','Series'), 
            _t('table','Num'), 
            _t('table','Tags'), 
            _t('table','Lang'), 
            _t('table','Translator'), 
            _t('table','Type'), 
            _t('table','File')
        ]
        self.hidden_column_width = [250] * len(self.headers)

        for i in range(len(self.headers)):
            model.setHeaderData(i, Qt.Horizontal, self.headers[i])

        self.setModel(model)
        self.hideColumn(0)
        self.horizontalHeader().setSectionsMovable(True)
        self.setItemDelegate(StyledItemDelegate())

        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self.onHeaderContextMenu)
        

    def onHeaderContextMenu(self, point):
        menu = QMenu()

        for i in range(len(self.headers))[1:]:
            item = QAction(self.headers[i], parent=menu, checkable=True, checked=not self.isColumnHidden(i))
            item.setData(i)
            menu.addAction(item)

        action = menu.exec(self.mapToGlobal(point))
        if action:
            column = action.data()
            if self.isColumnHidden(column):
                self.showColumn(column)
                width = self.hidden_column_width[column] if self.hidden_column_width[column] > 0 else 250
                self.setColumnWidth(column, width)
            else:
                self.hidden_column_width[column] = self.columnWidth(column)
                self.hideColumn(column) 

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

    def getColumnsWidth(self):
        widths = []
        for i in range(self.horizontalHeader().count()):
            widths.append(self.columnWidth(i))
        return widths

    def setColumnsWidth(self, widths):
        for i in range(len(widths)):
            self.setColumnWidth(i, widths[i])

    def getColumnsOrder(self):
        orders = []
        for i in range(self.horizontalHeader().count()):
            orders.append({'logical': i, 'visual': self.horizontalHeader().visualIndex(i)})
        return orders

    def setColumnsOrder(self, orders):
        for order in orders:
            vi = self.horizontalHeader().visualIndex(order['logical'])
            self.horizontalHeader().moveSection(vi, order['visual'])

    def getHiddenColumns(self):
        hidden = []
        for i in range(self.horizontalHeader().count()):
            hidden.append({'column': i, 'is_hidden': self.isColumnHidden(i)})
        return hidden

    def setHiddenColumns(self, hidden):
        if hidden:
            for h in hidden:
                if h['is_hidden']:
                    self.hideColumn(h['column'])
                else:
                    self.showColumn(h['column'])


    def setHiddenColumnsWidth(self, width):
        if len(width) == len(self.hidden_column_width):
            self.hidden_column_width = width

    def getHiddenColumnsWidth(self):
        return self.hidden_column_width

    def selectAll(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        while self.model().canFetchMore():
            self.model().fetchMore()
        QApplication.restoreOverrideCursor()
        return super().selectAll()


class StyledItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        itemOption = QStyleOptionViewItem(option)
        if itemOption.state and QStyle.State_HasFocus:
            itemOption.state = itemOption.state & ~QStyle.State_HasFocus
        return super(StyledItemDelegate, self).paint(painter, itemOption, index)


class BookTableModel(QSqlTableModel):
    def __init__(self, parent=None, db=None):
        super(BookTableModel, self).__init__(parent, db)
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)

    def data(self, index, role):
        if role == Qt.ToolTipRole:
            return super(BookTableModel, self).data(index, Qt.DisplayRole)
        
        return super(BookTableModel, self).data(index, role)