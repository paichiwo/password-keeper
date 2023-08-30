import os.path
from src.database import Database
from src.login_window import LoginApp


def main():
    """Initialize a database and create a login window"""
    if not os.path.exists('./db/db.db'):
        Database().create_db()

        print("database created")
    else:
        print("database exists, proceeding...")

    login_app = LoginApp()
    login_app.mainloop()

    Database().close_db()


if __name__ == "__main__":
    main()
