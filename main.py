from src.database import Database
from src.login_window import LoginApp


def main():
    """Initialize a database and create a login window"""
    Database().create_db()
    LoginApp().mainloop()
    Database().close_db()


if __name__ == "__main__":
    main()
