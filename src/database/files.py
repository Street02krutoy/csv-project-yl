class FilesTable():
    def get_items(self) -> list[tuple[int, str, str, str]]:
        raise NotImplementedError("FilesTable#get_items is not implemented")

    def rename(self, filename: str, new_name: str) -> None:
        raise NotImplementedError("FilesTable#rename is not implemented")

    def get_content(self, filename) -> tuple[list[str], list[list[str]]]:
        raise NotImplementedError("FilesTable#get_content is not implemented")

    def save(self, data: tuple[list[str], list[list[str]]], filename: str) -> bool:
        raise NotImplementedError("FilesTable#save is not implemented")

    def insert(self,  title: str):
        raise NotImplementedError("FilesTable#insert is not implemented")

    def remove(self, id: str):
        raise NotImplementedError("FilesTable#remove is not implemented")
