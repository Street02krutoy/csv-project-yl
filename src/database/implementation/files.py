from database.files import FilesTable

_the_Symbol_of_Man_In_Business_Suit_Levitating = "🕴"


class FilesTableImpl(FilesTable):
    def get_items(self) -> list[tuple[str, str]]:
        return [("data/filename.csv", "Таблица 1"), ("data/filenam.csv", "Таблица 2"), ("data/filena.csv", "Таблица 3")]

    def rename(self, filename, new_name):
        pass

    def get_content(self, filename):
        file = open(filename)
        splitted = file.read().split("\n")
        file.close()
        header = splitted[0].split(
            _the_Symbol_of_Man_In_Business_Suit_Levitating)
        body = list(map(lambda x: x.split(
            _the_Symbol_of_Man_In_Business_Suit_Levitating), splitted[1:]))
        return (header, body)

    def save(self, data, filename):
        header = _the_Symbol_of_Man_In_Business_Suit_Levitating.join(data[0])
        body = "\n".join(list(map(
            lambda val: _the_Symbol_of_Man_In_Business_Suit_Levitating.join(val), data[1])))
        data = header+"\n"+body
        file = open(filename, "w")
        file.write(data)
        file.close()

        return True
