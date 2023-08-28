import tkinter
from tkinter import ttk
import customtkinter as ctk
from PIL import Image


class PasswordKeeper(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("./img/icon_512x512.ico")
        self.title("Password Keeper")
        self.geometry("450x450")

        self.frame_top = None
        self.search_entry = None
        self.search_btn = None
        self.search_btn_img = None
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

        # --- SEARCH FRAME ---
        self.frame_top = ctk.CTkFrame(self)
        self.frame_top.pack(padx=20, fill='both', anchor='center')
        self.frame_top.columnconfigure(0, weight=1)
        self.frame_top.rowconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(self.frame_top, placeholder_text="Search")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.search_btn_img = ctk.CTkImage(Image.open("./img/search.png"))
        self.search_btn = ctk.CTkButton(self.frame_top, image=self.search_btn_img, text="", fg_color='transparent', width=30)
        self.search_btn.grid(row=0, column=1, padx=10, sticky='ew')

        # --- INPUT FRAME ---
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill='both', expand=True, anchor='center')
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)

        self.user_web = ctk.CTkEntry(self.frame, placeholder_text="Website")
        self.user_web.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.user_name = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.user_name.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.user_pass = ctk.CTkEntry(self.frame, placeholder_text="Password")
        self.user_pass.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        self.save_btn = ctk.CTkButton(self.frame, text="Save Account")
        self.save_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.generate_btn = ctk.CTkButton(self.frame, text="Generate")
        self.generate_btn.grid(row=1, column=2, padx=10, sticky='ew')

