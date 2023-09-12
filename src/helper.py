import re
import random
from string import ascii_lowercase, ascii_uppercase, digits
from password_strength import PasswordStats as ps


class Helper:
    def __init__(self):
        self.allowed_password_characters = ascii_uppercase + ascii_lowercase + digits + '!@#$&-_.,{}%+'

    @staticmethod
    def center_window(window, width, height):
        """Center a window on the screen using the provided dimensions"""
        x = (window.winfo_screenwidth() - width) // 2
        y = (window.winfo_screenheight() - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
        window.update_idletasks()

    @staticmethod
    def is_valid_email(email):
        """Check for a valid email address format"""
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email)

    @staticmethod
    def password_strength(password):
        """Return password strength in float; anything above 0.5 is a good password, over 0.8 perfect password"""
        if password:
            stats = ps(password)
            pass_strength = round(stats.strength(), 3)
            return pass_strength

    def is_valid_password(self, password):
        """Check for valid password"""
        for letter in password:
            if letter not in self.allowed_password_characters:
                return False
        return True

    def generate_password(self, password_length):
        """Generate passwords between 14 and 20 characters long using letters, numbers and symbols"""
        password = "".join(random.choices(self.allowed_password_characters, k=password_length))
        return password
