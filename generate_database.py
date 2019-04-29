import sqlite3


class DataBase:
    def __init__(self):
        """
        Create table Users
        """
        db = sqlite3.connect('db.sqlite3')
        conn = db.cursor()
        conn.execute('CREATE TABLE IF NOT EXISTS Users('
                     'user_id INTEGER NOT NULL UNIQUE,'
                     'is_active BOOLEAN DEFAULT 1)'
                     )


if __name__ == "__main__":
    DataBase()
