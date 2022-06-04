from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem
from PyQt5.QtCore import Qt
import ebookmeta
import os

class BookTreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(BookTreeWidget, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.clear()
        self.headerItem().setText(0, "Title")
        self.headerItem().setText(1, "Author")
        self.headerItem().setText(2, "Series")
        self.headerItem().setText(3, "Number")
        self.headerItem().setText(4, "Type")
        self.headerItem().setText(5, "Tags")
        self.headerItem().setText(6, "Lang")
        self.headerItem().setText(7, "File")
        self.headerItem().setText(8, "Path")

        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)

    def selectAll(self):
        root = self.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setSelected(True)


    def removeSelected(self):
        root = self.invisibleRootItem()
        for item in self.selectedItems():
            root.removeChild(item)


    def addItem(self, meta: ebookmeta.Metadata):
        found = False
        root = self.invisibleRootItem()

        for i in range(root.childCount()):
            if root.child(i).data(0, Qt.UserRole) == meta.file:
                found = True
                break
        
        if not found:
            (path, file) = os.path.split(meta.file)
            
            item = QTreeWidgetItem()
            item.setText(0, meta.title)
            item.setText(1, meta.get_author_string())
            item.setText(2, meta.series)
            item.setText(3, meta.series_index)
            item.setText(4, meta.format)
            item.setText(5, meta.get_tag_description_string())
            item.setText(6, meta.lang)
            item.setText(7, file)
            item.setText(8, path)
            item.setData(0, Qt.UserRole, meta.file)
            self.addTopLevelItem(item)

        
    