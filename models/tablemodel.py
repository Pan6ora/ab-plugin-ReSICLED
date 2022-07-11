import operator
from PySide2.QtCore import *
from PySide2.QtGui import *


class TableModel(QAbstractTableModel):
    """
    Generic table model that will be used to display tables in the recicled tables
    """
    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        """
        Returns the number of rows
        """
        return len(self.mylist)

    def columnCount(self, parent):
        """
        Returns the number of columns
        """
        return len(self.mylist[0])

    def data(self, index, role):
        """
        returns the data that has to be printed in each cell
        @param index : the cell coordinates in the table
        @param role : visibility status (if set as DisplayRole, you display it, otherwise you don't)
        """
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.emit(SIGNAL("layoutChanged()"))