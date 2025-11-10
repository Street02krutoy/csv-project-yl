from PyQt6 import QtWidgets

from router.screen import AbstractRouter


class TestScreenWidget(QtWidgets.QWidget):
    def __init__(self, router=AbstractRouter, *args):
        super().__init__()
        self.router = router
        layout = QtWidgets.QVBoxLayout(self)

        self.slash_button = QtWidgets.QPushButton()
        self.slash_button.clicked.connect(self.go_to_slash)
        self.slash_button.setText("Go to /")

        self.back_button = QtWidgets.QPushButton()
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setText("Go back")

        layout.addWidget(self.slash_button)
        layout.addWidget(self.back_button)

    def go_to_slash(self):
        self.router.route_to("/")

    def go_back(self):
        self.router.route_back()
