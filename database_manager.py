import sqlite3

class DatabaseManager:
    def __init__(self, db_path="data.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE)""")
            self.conn.execute("""CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL)""")

    def add_contact(self, name, phone):
        with self.conn:
            self.conn.execute("INSERT OR IGNORE INTO contacts (name, phone) VALUES (?, ?)", (name, phone))

    def add_message(self, title, content):
        with self.conn:
            self.conn.execute("INSERT INTO messages (title, content) VALUES (?, ?)", (title, content))

    def get_contacts(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name, phone FROM contacts")
        return cur.fetchall()

    def get_messages(self):
        cur = self.conn.cursor()
        cur.execute("SELECT title, content FROM messages")
        return cur.fetchall()
