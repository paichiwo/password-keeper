import os
import sqlite3
import sys


def resource_path(relative_path):
    """Get the absolute path to a resource, accommodating both development and PyInstaller builds"""

    if hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class Database:
    """Database manipulation methods"""
    def __init__(self):
        self.SQL_FILEPATH = resource_path('db/db.sql')
        self.DB_FILEPATH = resource_path('db/db.db')

        self.conn = sqlite3.connect(self.DB_FILEPATH)
        self.cursor = self.conn.cursor()

    def create_db(self):
        """Create a new database using an .sql file"""
        with open(self.SQL_FILEPATH, "r", encoding='utf-8') as sql_file:
            sql_commands = sql_file.read()
        try:
            self.cursor.executescript(sql_commands)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)

    def create_user(self, email, password):
        """Save user data to database"""
        insert_query = "INSERT INTO user_profile (email, password) VALUES (?, ?);"
        self.cursor.execute(insert_query, (email, password))
        self.conn.commit()

    def validate_user(self, email, password):
        """Validate user credentials"""
        select_query = "SELECT * FROM user_profile WHERE email = ? AND password = ?;"
        self.cursor.execute(select_query, (email, password))
        user_data = self.cursor.fetchone()
        if user_data:
            return True
        else:
            return False

    def close_db(self):
        """Close the database connection"""
        self.conn.close()
