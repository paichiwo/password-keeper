import customtkinter as ctk
import sqlite3
from tkinter import BOTTOM
from PIL import Image
from src.user import User
from src.helper import Helper
from src.database import Database
from src.password_keeper import PasswordKeeper


class LoginApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_default_color_theme("./data/paichiwo_theme.json")
        self.title("Login Window")
        self.iconbitmap("./img/icon_512x512.ico")
        Helper().center_window(self, 550, 500)

        self.frame = None
        self.frame_label = None
        self.user_entry = None
        self.user_pass = None
        self.confirm_user_pass = None
        self.login_button = None
        self.remember_me = None
        self.msg_label = None
        self.signup_button = None
        self.cancel_button = None

        self.root_label_img = ctk.CTkImage(Image.open("./img/password_keeper_logo_345x30.png"), size=(345, 30))
        self.root_label = ctk.CTkLabel(self, image=self.root_label_img, text="", fg_color='transparent')
        self.root_label.pack(pady=20)

        self.login_frame()

    def login_frame(self):
        """Create UI elements for the login frame"""
        if self.frame:
            self.frame.destroy()

        self.frame = ctk.CTkFrame(master=self, fg_color='transparent')
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.frame_label = ctk.CTkLabel(
            master=self.frame,
            text="Use your existing account or create one to get access",
            text_color='grey')
        self.frame_label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Email", width=200)
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=200)
        self.user_pass.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(
            master=self.frame,
            text='Login', width=200,
            command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.remember_me = ctk.CTkCheckBox(master=self.frame, text='Remember Me')
        self.remember_me.pack(pady=12, padx=10)

        self.msg_label = ctk.CTkLabel(self.frame, text="", text_color='pink')
        self.msg_label.pack(pady=12, padx=10)

        self.signup_button = ctk.CTkButton(
            master=self.frame,
            text='Sign Up',
            width=200,
            command=self.signup)
        self.signup_button.pack(pady=24, padx=10, side=BOTTOM)

    def signup_frame(self):
        """Create UI elements for the user registration frame"""
        if self.frame:
            self.frame.destroy()

        self.frame = ctk.CTkFrame(master=self, fg_color='transparent')
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.frame_label = ctk.CTkLabel(master=self.frame, text='Create your account', text_color='grey')
        self.frame_label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Email", width=200)
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=200)
        self.user_pass.pack(pady=12, padx=10)

        self.confirm_user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Confirm", show="*", width=200)
        self.confirm_user_pass.pack(pady=12, padx=10)

        self.signup_button = ctk.CTkButton(
            master=self.frame,
            text='Create Account',
            width=200,
            command=self.add_user)
        self.signup_button.pack(pady=12, padx=10)

        self.msg_label = ctk.CTkLabel(self.frame, text="", text_color="grey")
        self.msg_label.pack(pady=12, padx=10)

        self.cancel_button = ctk.CTkButton(
            master=self.frame,
            text='Go Back',
            width=200,
            command=self.go_back)
        self.cancel_button.pack(pady=24, padx=10, side=BOTTOM)

    def login(self):
        """Login button callback"""

        # get user data
        email = self.user_entry.get()
        password = self.user_pass.get()

        # if user data valid -> login
        if Helper().is_valid_email(email=self.user_entry.get()):
            user_id = Database().validate_user(email, password)
            if user_id:
                self.frame.destroy()
                self.frame = PasswordKeeper(self, fg_color='transparent')
                self.frame.pack(fill='both', expand=True)
                User().save_user_session(user_id)
            else:
                self.msg_label.configure(text="Wrong credentials")
        else:
            self.msg_label.configure(text="Enter valid email address")

    def signup(self):
        """Show Sign Up frame"""
        self.signup_frame()

    def add_user(self):
        """Add a user to the database"""

        # get user data
        email = self.user_entry.get()
        password = self.user_pass.get()
        password_confirmation = self.confirm_user_pass.get()

        # validate the user data
        if password != password_confirmation:
            self.msg_label.configure(text="Passwords do not match")
            return

        if not Helper().is_valid_email(email):
            self.msg_label.configure(text="Please enter a valid email address")
            return

        if Database().user_exists(email):
            self.msg_label.configure(text="Account exists!\nGo back to log in")
            return

        if len(password) < 6:
            self.msg_label.configure(text="Password must be a minimum of 6 characters")
            return

        if not Helper().is_valid_password(password):
            specials = '!@#$&-_.,{}%+'
            self.msg_label.configure(text=f"Allowed characters:\nuppercase, lowercase, digits, {specials}")
            return

        # create a user account
        try:
            Database().create_user(email, password)
            self.msg_label.configure(text="SUCCESS !\nGo back to log in")
        except sqlite3.Error as error:
            self.msg_label.configure(text=f"SQLite Error: {error}")

    def go_back(self):
        """Show login frame"""
        self.login_frame()
