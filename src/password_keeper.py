import customtkinter as ctk
from tkinter import END
import tkinter as tk
from CTkTable import CTkTable
from PIL import Image
from src.database import Database
from src.helpers import load_user_session, generate_password, password_strength


class PasswordKeeper(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_frame = None

        self.search_frame = None
        self.search_entry = None
        self.search_btn_img = None
        self.search_btn = None
        self.user_frame = None
        self.user_web = None
        self.user_name = None
        self.user_pass = None
        self.slider = None
        self.pass_length_label = None
        self.generate_btn = None
        self.pass_info_label = None
        self.save_btn = None
        self.table_frame = None
        self.table = None

        self.pass_info_var = tk.StringVar()
        self.pass_length_var = tk.StringVar()

        self.password_keeper_frame()

    def password_keeper_frame(self):

        self.main_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.main_frame.pack(fill='both', expand=True)

        # --- SEARCH FRAME ---
        self.search_frame = ctk.CTkFrame(self.main_frame)
        self.search_frame.pack(padx=20, pady=20, fill='both', anchor='center')
        self.search_frame.columnconfigure(0, weight=1)
        self.search_frame.rowconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.search_btn_img = ctk.CTkImage(Image.open("./img/search.png"))
        self.search_btn = ctk.CTkButton(self.search_frame, image=self.search_btn_img, text="", fg_color='transparent', width=20, command=self.search)
        self.search_btn.grid(row=0, column=1, padx=10, sticky='ew')

        # --- INPUT FRAME ---
        self.user_frame = ctk.CTkFrame(self.main_frame)
        self.user_frame.pack(padx=20, fill='both', anchor='center')
        self.user_frame.columnconfigure(0, weight=1)
        self.user_frame.columnconfigure(1, weight=1)
        self.user_frame.columnconfigure(2, weight=1)

        self.user_web = ctk.CTkEntry(self.user_frame, placeholder_text="Website")
        self.user_web.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.user_name = ctk.CTkEntry(self.user_frame, placeholder_text="Username")
        self.user_name.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.user_pass = ctk.CTkEntry(self.user_frame, placeholder_text="Password")
        self.user_pass.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
        self.user_pass.bind("<KeyRelease>", self.update_string_var)

        self.slider = ctk.CTkSlider(self.user_frame, from_=6, to=20, width=150, command=self.show_pass_length)
        self.slider.set(6)
        self.slider.grid(row=1, column=0, padx=10)

        self.pass_length_label = ctk.CTkLabel(self.user_frame, text="6 characters",  textvariable=self.pass_length_var, text_color='grey')
        self.pass_length_label.grid(row=1, column=1)

        self.generate_btn = ctk.CTkButton(self.user_frame, text="Generate", command=self.generate)
        self.generate_btn.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

        self.pass_info_label = ctk.CTkLabel(self.user_frame, text="test", textvariable=self.pass_info_var)
        self.pass_info_label.grid(row=2, column=0, padx=10, columnspan=2)

        self.save_btn = ctk.CTkButton(self.user_frame, text="Save Account", command=self.save_account)
        self.save_btn.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

        # --- TABLE FRAME ---
        self.table_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.table_frame.pack(padx=20, pady=20, fill='both', expand=True)

        headers = [["WEBSITE", "USERNAME", "PASSWORD"]]
        self.table = CTkTable(master=self.table_frame, corner_radius=7, row=1, values=headers, header_color=("#8f8f8f", "#1f1f1f"))
        self.table.pack(fill="both", padx=2, pady=3)

    def save_account(self):
        """Save user account to the database"""

        # get required data
        user_id = load_user_session()
        website = self.user_web.get()
        username = self.user_name.get()
        password = self.user_pass.get()

        # save database
        Database().save_user_data(user_id, website, username, password)
        print(f"data for website: [{website}] saved, user_id used: [{user_id}]")

    def search(self):
        """Populate the table and create as many rows as entries to display"""

        # get the results for search
        user_id = load_user_session()
        search_query = self.search_entry.get()
        if not search_query:
            results = Database().show_all(user_id)
        else:
            results = Database().search(user_id, search_query)

        # clear the existing table
        if len(self.table.get()) > 1:
            for n in range(1, len(self.table.get())):
                self.table.delete_row(n)

        # update the table
        for i, account in enumerate(results):
            self.table.add_row(account, i + 1)

    def generate(self):
        """Generate password between 14 and 20 characters long using letters,
        numbers and symbols, show password length and password info"""

        # generate password and update user_pass entry
        password = generate_password(int(self.slider.get()))
        self.user_pass.delete(0, END)
        self.user_pass.insert(0, password)

        # update password length and password info
        pass_strength = password_strength(password)
        self.pass_info_var.set(f"Password strength: {pass_strength}")
        self.pass_length_var.set(f"{str(len(password))} characters")

    def show_pass_length(self, slider_value):
        """Show pass length according to slider"""
        self.pass_length_var.set(f"{int(slider_value)} characters")

    def update_string_var(self, event):
        """Update tk string variables"""
        password = self.user_pass.get()
        pass_strength = password_strength(password)
        self.pass_info_var.set(f"Password strength: {pass_strength}")
        self.pass_length_var.set(f"{str(len(password))} characters")
