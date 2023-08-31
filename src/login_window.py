import sqlite3
import customtkinter as ctk
from tkinter import BOTTOM
from src.helpers import center_window, is_valid_email, is_valid_password, save_user_session
from src.database import Database
from src.password_keeper import PasswordKeeper


class LoginApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Login Window")
        self.iconbitmap("./img/icon_512x512.ico")
        center_window(self, 550, 500)

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

        self.root_label = ctk.CTkLabel(self, text="Password Keeper", font=("Any", 26, "bold"))
        self.root_label.pack(pady=20)

        self.login_frame()

    def login_frame(self):
        """Create UI elements for the login frame"""
        if self.frame:
            self.frame.destroy()

        self.frame = ctk.CTkFrame(master=self, fg_color='transparent')
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.frame_label = ctk.CTkLabel(master=self.frame, text='Login')
        self.frame_label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Email", width=200)
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=200)
        self.user_pass.pack(pady=12, padx=10)

        self.login_button = ctk.CTkButton(master=self.frame, text='Login', width=200, command=self.login)
        self.login_button.pack(pady=12, padx=10)

        self.remember_me = ctk.CTkCheckBox(master=self.frame, text='Remember Me')
        self.remember_me.pack(pady=12, padx=10)

        self.msg_label = ctk.CTkLabel(self.frame, text="")
        self.msg_label.pack(pady=12, padx=10)

        self.signup_button = ctk.CTkButton(master=self.frame, text='Sign Up', width=200, command=self.signup)
        self.signup_button.pack(pady=24, padx=10, side=BOTTOM)

    def signup_frame(self):
        """Create UI elements for the user registration frame"""
        if self.frame:
            self.frame.destroy()

        self.frame = ctk.CTkFrame(master=self, fg_color='transparent')
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.frame_label = ctk.CTkLabel(master=self.frame, text='Sign up')
        self.frame_label.pack(pady=12, padx=10)

        self.user_entry = ctk.CTkEntry(master=self.frame, placeholder_text="Email", width=200)
        self.user_entry.pack(pady=12, padx=10)

        self.user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Password", show="*", width=200)
        self.user_pass.pack(pady=12, padx=10)

        self.confirm_user_pass = ctk.CTkEntry(master=self.frame, placeholder_text="Confirm", show="*", width=200)
        self.confirm_user_pass.pack(pady=12, padx=10)

        self.signup_button = ctk.CTkButton(master=self.frame, text='Create Account', width=200, command=self.add_user)
        self.signup_button.pack(pady=12, padx=10)

        self.msg_label = ctk.CTkLabel(self.frame, text="Enter email and password", text_color="grey")
        self.msg_label.pack(pady=12, padx=10)

        self.cancel_button = ctk.CTkButton(master=self.frame, text='Go Back', width=200, command=self.go_back)
        self.cancel_button.pack(pady=24, padx=10, side=BOTTOM)

    def login(self):
        """Login button callback"""
        email = self.user_entry.get()
        password = self.user_pass.get()

        if is_valid_email(self.user_entry.get()):
            user_id = Database().validate_user(email, password)
            print(f"user id: {user_id}")
            save_user_session(user_id)
            if user_id:
                self.frame.destroy()
                self.frame = PasswordKeeper(self, fg_color='transparent')
                self.frame.pack(fill='both', expand=True)

            else:
                self.msg_label.configure(text="Wrong credentials")
        else:
            self.msg_label.configure(text="Enter valid email address and password", text_color="grey")

    def signup(self):
        """Show Sign Up frame"""
        self.signup_frame()

    def add_user(self):
        """Add a user to the database"""
        email = self.user_entry.get()
        password = self.user_pass.get()
        password_confirmation = self.confirm_user_pass.get()

        if password == password_confirmation:
            if is_valid_email(email):
                if len(password) >= 6:
                    if is_valid_password(password):
                        try:
                            Database().create_user(email, password)
                        except sqlite3.Error as error:
                            self.msg_label.configure(text=f"SQLite Error: {error}")
                        self.msg_label.configure(text="SUCCESS !\nGo back to log in")
                    else:
                        specials = "! @ # $ & - _"
                        self.msg_label.configure(text=f"Allowed characters:\nuppercase, lowercase, digits, {specials}")
                else:
                    self.msg_label.configure(text="Password must be minimum 6 characters")
            else:
                self.msg_label.configure(text="Please enter valid email address")
        else:
            self.msg_label.configure(text="Passwords don't match")

    def go_back(self):
        """Show login frame"""
        self.login_frame()
