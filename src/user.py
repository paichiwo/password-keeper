import os
import sys


def resource_path(relative_path):
    """Get the absolute path to a resource, accommodating both development and PyInstaller builds"""
    if hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


class User:
    """Creates a User object"""
    def __init__(self):
        self.user_session_path = 'data/session_data'
        self.user_session = None

        self.load_user_session()

    def save_user_session(self, user_id):
        """Save user_id from login as user session number"""
        with open(resource_path(self.user_session_path), 'w') as f:
            f.write(user_id)

    def load_user_session(self):
        """Load session number"""
        with open(resource_path(self.user_session_path), 'r') as f:
            self.user_session = f.read()
            return self.user_session
