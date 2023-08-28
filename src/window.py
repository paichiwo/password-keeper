from tkinter import CENTER

import customtkinter as ctk


class PasswordKeeper(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("./img/icon_512x512.ico")
        self.title("Password Keeper")
        self.geometry("450x450")

        self.frame_top = None
        self.user_web = None
        self.frame = None
        self.user_name = None
        self.user_pass = None
        self.save_btn = None
        self.generate_btn = None

        self.root_label = ctk.CTkLabel(self, text="LOGO")
        self.root_label.pack(padx=10, pady=10)

        self.password_keeper_frame()

    def password_keeper_frame(self):

        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(padx=20, fill='both', anchor='center')

        self.user_web = ctk.CTkEntry(self.frame_top, placeholder_text="Website")
        self.user_web.pack(padx=20, pady=20, fill='x')
