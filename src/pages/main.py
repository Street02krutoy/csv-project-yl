from PyQt6 import QtWidgets, QtGui, QtCore

from database.files import FilesTable
from router.screen import AbstractRouter


class MainScreenWidget(QtWidgets.QWidget):
    def __init__(self, router=AbstractRouter, *args):
        super().__init__()
        self.router = router
        self.router.get_main_window().setWindowTitle("Выбор таблицы")
        self.router.get_main_window().setMinimumSize(0, 0)
        self.init_menu()

        layout = QtWidgets.QGridLayout(self)

        self.list_view = QtWidgets.QListView()
        self.model = QtGui.QStandardItemModel()
        self.items = self.router.get_files_table().get_items()
        for item in self.items:
            self.model.appendRow(QtGui.QStandardItem(str(item[1])))
        self.list_view.setModel(self.model)

        self.model.itemChanged.connect(self.on_item_changed)

        self.button = QtWidgets.QPushButton()
        self.button.clicked.connect(lambda: self.router.route_to(
            "/document", *self.items[self.list_view.currentIndex().row()]))
        self.button.setText("Перейти к таблице")

        layout.addWidget(self.list_view)
        layout.addWidget(self.button)

    def init_menu(self):
        menu_bar = self.router.get_main_window().menuBar()

        file_menu = menu_bar.addMenu("File")

        open_action = QtGui.QAction("Open", self)
        new_action = QtGui.QAction("New", self)

        file_menu.addAction(open_action)
        file_menu.addAction(new_action)

        # open_action.triggered.connect(self.save)
        new_action.triggered.connect(self.create_file)

        open_action.setShortcut(QtGui.QKeySequence.StandardKey.Open)
        new_action.setShortcut(QtGui.QKeySequence.StandardKey.New)

    def create_file(self):
        file, ok = QtWidgets.QInputDialog.getText(
            self,
            "Enter the filename",
            "Filename:"
        )
        self.router.get_files_table().insert(file)
        self.items = self.router.get_files_table().get_items()
        print(self.items)
        self.model = QtGui.QStandardItemModel()
        for item in self.items:
            self.model.appendRow(QtGui.QStandardItem(str(item[1])))
        self.list_view.setModel(self.model)

    def on_item_changed(self, item: QtGui.QStandardItem):
        row = item.row()
        new_text = item.text()
        filename = self.items[row][0]
        self.router.get_files_table().rename(filename, new_text)
