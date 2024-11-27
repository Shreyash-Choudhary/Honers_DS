import sqlite3

class DatabaseHandler:
    def __init__(self, db_name='feedback.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            feedback_comment TEXT,
            sentiment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_feedback(self, name, comment, sentiment):
        query = """
        INSERT INTO feedback (name, feedback_comment, sentiment)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (name, comment, sentiment))
        self.conn.commit()

    def fetch_all_feedback(self):
        query = "SELECT * FROM feedback"
        return self.conn.execute(query).fetchall()
