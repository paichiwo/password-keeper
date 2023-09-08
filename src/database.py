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
        if not os.path.exists(self.DB_FILEPATH):
            with open(self.SQL_FILEPATH, "r", encoding='utf-8') as sql_file:
                sql_commands = sql_file.read()
            try:
                self.cursor.executescript(sql_commands)
                self.conn.commit()
                print("Database created")
            except sqlite3.Error as e:
                print(e)
        else:
            print("Database exists, proceeding...")

    def user_exists(self, email):
        """Check if user exists in the database"""
        check_query = "SELECT COUNT(*) FROM user_profile WHERE email = ?;"
        self.cursor.execute(check_query, (email,))
        existing_account_count = self.cursor.fetchone()[0]
        return existing_account_count > 0

    def create_user(self, email, password):
        """Save user data to database"""
        insert_query = "INSERT INTO user_profile (email, password) VALUES (?, ?);"
        self.cursor.execute(insert_query, (email, password))
        self.conn.commit()

    def validate_user(self, email, password):
        """Validate user credentials"""
        select_query = "SELECT * FROM user_profile WHERE email = ? AND password = ?;"
        self.cursor.execute(select_query, (email, password))
        login_data = self.cursor.fetchone()
        if login_data:
            user_id = login_data[0]
            return str(user_id)
        else:
            return False

    def save_user_data(self, user_id, website, username, password):
        """Save user data to the user_data table in the database"""
        insert_query = "INSERT INTO user_data (user_id, website, username, password) VALUES (?, ?, ?, ?);"
        self.cursor.execute(insert_query, (user_id, website, username, password))
        self.conn.commit()

    def show_all(self, user_id):  # need to add a search query
        """Search database for user query using user session"""
        check_query = "SELECT * FROM user_data WHERE user_id = ?;"
        self.cursor.execute(check_query, (user_id,))
        result = self.cursor.fetchall()
        new_list = [list(entry[2:]) for entry in result]
        return new_list

    def search(self, user_id, search_query):
        """Search database for user query using user session"""
        check_query = "SELECT * FROM user_data WHERE user_id = ? AND (website LIKE ? OR username LIKE ? OR password LIKE ?);"
        search_query = f"%{search_query}%"
        self.cursor.execute(check_query, (user_id, search_query, search_query, search_query))
        result = self.cursor.fetchall()
        new_list = [list(entry[2:]) for entry in result]
        return new_list

    def close_db(self):
        """Close the database connection"""
        self.conn.close()
