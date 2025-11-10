import sys
from PyQt6 import QtGui, QtWidgets, QtCore

from loaders.styles import load_styles
from router.router import ApplicationRouter


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_css()

    def load_css(self):
        self.setStyleSheet(load_styles())


def run_app(argv=None):
    app = QtWidgets.QApplication(argv or sys.argv)
    w = ApplicationWindow()
    router = ApplicationRouter(w)
    router.route_to("/")
    w.show()
    return app.exec()


if __name__ == "__main__":
    run_app()
    exit()
