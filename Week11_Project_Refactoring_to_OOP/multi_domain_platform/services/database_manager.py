import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        """Connect to the SQLite database if not already connected."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def fetch_all(self, sql, params=()):
        """Fetch all rows from a query."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()

    def fetch_one(self, sql, params=()):
        """Fetch a single row from a query."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    def execute_query(self, sql, params=()):
        """Execute a query (INSERT, UPDATE, DELETE)."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        conn.commit()
        return cur

    def close(self):
        """Close the database connection."""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
