import re
import string


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
