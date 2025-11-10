from PyQt6 import QtWidgets, QtGui, QtCore

from router.screen import AbstractRouter


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if orientation == QtCore.Qt.Orientation.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)

    def flags(self, index):
        # Make all cells selectable, enabled, and editable
        return QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role=QtCore.Qt.ItemDataRole.EditRole):
        if role == QtCore.Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            # Notify the view that data changed
            self.dataChanged.emit(
                index, index, [QtCore.Qt.ItemDataRole.DisplayRole])
            return True
        return False

    def setHeaderData(self, section, orientation, value, role=QtCore.Qt.ItemDataRole.EditRole):
        if role == QtCore.Qt.ItemDataRole.EditRole and orientation == QtCore.Qt.Orientation.Horizontal:
            self._headers[section] = value
            self.headerDataChanged.emit(orientation, section, section)
            return True
        return False


class DocumentScreenWidget(QtWidgets.QWidget):
    def __init__(self, router=AbstractRouter, *args):
        super().__init__()
        self.router = router
        self.hasUnsavedChanges = False

        self.name = args[1]
        self.filename = args[0]

        self.router.get_main_window().setWindowTitle(args[1])
        self.router.get_main_window().setMinimumSize(600, 400)
        self.init_menu()

        self.file_contents = self.router.get_files_table().get_content(args[0])

        self.model = TableModel(self.file_contents[1], self.file_contents[0])
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def init_menu(self):
        menu_bar = self.router.get_main_window().menuBar()

        file_menu = menu_bar.addMenu("File")

        save_action = QtGui.QAction("Save", self)
        edit_headers_action = QtGui.QAction("Edit headers", self)
        close_action = QtGui.QAction("Close", self)

        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        file_menu.addAction(edit_headers_action)

        save_action.triggered.connect(self.save)
        close_action.triggered.connect(self.close)

        save_action.setShortcut(QtGui.QKeySequence.StandardKey.Save)
        close_action.setShortcut(QtGui.QKeySequence.StandardKey.Close)
        edit_headers_action.setShortcut(QtGui.QKeySequence.StandardKey.New)

    def save(self):
        headers = self.model._headers
        body = []
        for row in range(self.model.rowCount(None)):
            row_data = []
            for col in range(self.model.columnCount(None)):
                index = self.model.index(row, col)
                row_data.append(self.model.data(
                    index, QtCore.Qt.ItemDataRole.DisplayRole))
            body.append(row_data)
        data = (headers, body)
        res = self.router.get_files_table().save(data, self.filename)
        if (res):
            self.hasUnsavedChanges = False

    def close(self):
        if self.hasUnsavedChanges:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Внимание")
            msg.setText(
                "У вас есть несохранённые данные, отменить изменения и выйти?")
            msg.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            msg.setWindowFlags(
                msg.windowFlags() & ~QtCore.Qt.WindowType.WindowContextHelpButtonHint
            )

            reply = msg.exec()

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                self.router.route_back()
        else:
            self.router.route_back()
