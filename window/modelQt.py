# -*- coding: utf-8 -*-

from PyQt4 import QtCore
import base64

class CustomModel(QtCore.QAbstractTableModel):
    def __init__(self, columns, parent=None,select=False):
        super(CustomModel, self).__init__(parent)
        self.columns = columns
        self.datatable = []
        self.select=False

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.datatable)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.columns[section].title()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            row = self.datatable[index.row()]
            column_key = self.columns[index.column()]
            if isinstance(row[column_key],bytes):
                if column_key == 'user_info':
                    return base64.b64decode(row[column_key]).decode("utf-8")
                return row[column_key].decode("utf-8")
            elif isinstance(row[column_key],list):
                return ",".join(row[column_key])
            else:
                return str(row[column_key])
        else:
            return None

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable