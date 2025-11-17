import sqlite3
from database.files import FilesTable

_the_Symbol_of_Man_In_Business_Suit_Levitating = "🕴"


class FilesTableImpl(FilesTable):

    def __init__(self, db_path="files.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_items(self) -> list[tuple[int, str, str, str]]:
        rows = self.conn.execute(
            "SELECT id, created_at, updated_at, title FROM files").fetchall()
        return [(row["id"], row["title"], row["created_at"], row["updated_at"]) for row in rows]

    def rename(self, id, new_name):
        self.conn.execute("""
            UPDATE files
            SET title = ?, updated_at = datetime('now')
            WHERE id = ?
        """, (new_name, id))
        self.conn.commit()

    def get_content(self, filename):
        file = open(filename)
        splitted = file.read().split("\n")
        file.close()
        header = splitted[0].split(
            _the_Symbol_of_Man_In_Business_Suit_Levitating)
        body = list(map(lambda x: x.split(
            _the_Symbol_of_Man_In_Business_Suit_Levitating), splitted[1:]))
        return (header, body)

    def save(self, data, id):
        header = _the_Symbol_of_Man_In_Business_Suit_Levitating.join(data[0])
        body = "\n".join(list(map(
            lambda val: _the_Symbol_of_Man_In_Business_Suit_Levitating.join(val), data[1])))
        data = header+"\n"+body
        file = open(f"data/{id}.csv", "w")
        file.write(data)
        file.close()
        self.conn.execute("""
            UPDATE files
            SET updated_at = datetime('now')
            WHERE id = ?
        """, (id,))
        self.conn.commit()
        return True

    def insert(self, title: str):

        cur = self.conn.execute("""
            INSERT INTO files (title, created_at, updated_at)
            VALUES (?, datetime('now'), datetime('now'))
        """, (title,))
        self.conn.commit()
        file_id = cur.lastrowid
        file = open(f"data/{file_id}.csv", "w")
        file.write("header🕴header\n🕴")
        file.close()
        return cur.lastrowid
