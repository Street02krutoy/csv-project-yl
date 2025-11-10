from PyQt6 import QtWidgets

from database.files import FilesTable


class AbstractRouter():
    def __init__():
        raise NotImplementedError("AbstractRouter#__init__ is not implemented")

    def route_to(self, path: str, *args) -> None:
        raise NotImplementedError("AbstractRouter#route_to is not implemented")

    def route_back(self) -> None:
        raise NotImplementedError(
            "AbstractRouter#route_back is not implemented")

    def get_history(self) -> list[str]:
        raise NotImplementedError(
            "AbstractRouter#get_history is not implemented")

    def get_files_table(self) -> FilesTable:
        raise NotImplementedError(
            "AbstractRouter#get_files_table is not implemented")

    def get_main_window(self) -> QtWidgets.QMainWindow:
        raise NotImplementedError(
            "AbstractRouter#get_main_window is not implemented")


class ApplicationScreen():
    def __init__(self, router: AbstractRouter):
        self.router = router

    def get_widget(self, *args):
        raise NotImplementedError(
            "ApplicationScreen#get_widget is not implemented")
