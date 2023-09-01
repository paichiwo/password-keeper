import re
import string
import random


def center_window(window, width, height):
    """Center a window on the screen using the provided dimensions"""
    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2

    window.geometry(f"{width}x{height}+{x}+{y}")
    window.update_idletasks()


def is_valid_email(email):
    """Check for a valid email address format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)


def is_valid_password(password):
    """Check for valid password"""
    password_pattern = string.ascii_letters + string.digits + "!@#$&-_"
    for letter in password:
        if letter not in password_pattern:
            return False
    return True


def save_user_session(user_id):
    """Save user_id as user session number"""
    with open('./data/session_data', 'w') as file:
        file.write(user_id)


def load_user_session():
    """Load user session id"""
    with open('./data/session_data', 'r') as file:
        return file.read()


def generate_password(password_length):
    """Generate passwords between 14 and 20 characters long using letters, numbers and symbols"""
    allowed_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$&-_.,{}%+"
    password = "".join(random.choices(allowed_characters, k=password_length))
    return password

