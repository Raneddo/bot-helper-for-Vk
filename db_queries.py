import sqlite3


class DataBase:
    conn: sqlite3.Cursor
    db: sqlite3.Connection

    def __init__(self, conn, db):
        self.conn = conn
        self.db = db

    def add_user_to_db(self, user_id: int):
        self.conn.execute('INSERT OR IGNORE INTO Users(user_id) VALUES (?)', (user_id,))
        self.db.commit()

    def set_is_active(self, user_id: int):
        self.conn.execute("UPDATE Users SET is_active=1 WHERE user_id=?", (user_id,))
        self.db.commit()

    def set_is_not_active(self, user_id: int):
        self.conn.execute("UPDATE Users SET is_active=0 WHERE user_id=?", (user_id,))
        self.db.commit()

    def get_active(self):
        return self.conn.execute('SELECT user_id FROM Users WHERE is_active=1').fetchall()

    def get_all(self):
        return self.conn.execute('SELECT user_id FROM Users').fetchall()

    def get_deactivated(self):
        return self.conn.execute('SELECT user_id FROM Users WHERE is_active=0').fetchall()
