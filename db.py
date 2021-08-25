import sqlite3

#The portfolio is saved in a sqlite database,
#this class controls fetching, inserting, removing and updating that database.

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY, ticker, weighting)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts")
        rows = self.cur.fetchall()
        return rows

    def insert(self, ticker, weighting):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?)",
                         (ticker, weighting))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM parts WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, ticker, weighting):
        self.cur.execute("UPDATE parts SET ticker = ?, weighting = ?",
                         (ticker, weighting))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

