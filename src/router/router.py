from PyQt6 import QtGui, QtWidgets, QtCore

from database.implementation.files import FilesTableImpl
from pages.document import DocumentScreenWidget
from pages.main import MainScreenWidget
from pages.test import TestScreenWidget
from router.screen import AbstractRouter, ApplicationScreen


class ApplicationRouter(AbstractRouter):
    def __init__(self, app: QtWidgets.QMainWindow):
        self.app = app
        self.files_table = FilesTableImpl()
        self.history: list[tuple[str, tuple]] = []
        self.screens: dict[str, ApplicationScreen] = {
            "/": MainScreen(self), "/document": DocumentScreen(self)}
        self.not_found_screen = NotFoundScreen(self)

    def route_to(self, path: str, *args):
        self.history.append((path, args))
        self.app.setMenuBar(QtWidgets.QMenuBar())
        try:
            self.app.setCentralWidget(self.screens[path].get_widget(*args))
        except KeyError:
            self.app.setCentralWidget(self.not_found_screen.get_widget(*args))

    def route_back(self):
        self.history.pop()
        route = self.history[-1]
        self.app.setMenuBar(QtWidgets.QMenuBar())
        self.app.setCentralWidget(self.screens[route[0]].get_widget(*route[1]))

    def get_history(self):
        return list(map(lambda h: h[0], self.history))

    def get_files_table(self):
        return self.files_table

    def get_main_window(self):
        return self.app


class MainScreen(ApplicationScreen):
    def __init__(self, router):
        super().__init__(router)

    def get_widget(self, *args):
        return MainScreenWidget(self.router, *args)


class DocumentScreen(ApplicationScreen):
    def __init__(self, router):
        super().__init__(router)

    def get_widget(self, *args):
        return DocumentScreenWidget(self.router, *args)


class NotFoundScreen(ApplicationScreen):
    def __init__(self, router):
        super().__init__(router)

    def get_widget(self, *args):
        print(args)
        window = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(window)
        button = QtWidgets.QPushButton()
        button.clicked.connect(self.router.route_back)
        button.setText("Произошла ошибка. Назад?")
        layout.addWidget(button)

        return window
