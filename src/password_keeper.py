from CTkTable import CTkTable
import customtkinter as ctk
from PIL import Image
from src.database import Database
from src.helpers import load_user_session


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
        self.save_btn = None
        self.generate_btn = None
        self.table_frame = None
        self.table = None

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
        self.search_btn = ctk.CTkButton(self.search_frame, image=self.search_btn_img, text="", fg_color='transparent', width=20)
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

        self.save_btn = ctk.CTkButton(self.user_frame, text="Save Account", command=self.save_account)
        self.save_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

        self.generate_btn = ctk.CTkButton(self.user_frame, text="Generate", command=self.generate)
        self.generate_btn.grid(row=1, column=2, padx=10, sticky='ew')

        # TABLE FRAME
        self.table_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.table_frame.pack(padx=20, pady=20, fill='both', expand=True)

        headers = [["WEBSITE", "USERNAME", "PASSWORD"]]

        self.table = CTkTable(master=self.table_frame, corner_radius=7, row=1, values=headers, header_color=("#8f8f8f", "#1f1f1f"))
        self.table.pack(fill="both", padx=2, pady=3)

    def save_account(self):
        """Save user account to the database"""
        website = self.user_web.get()
        username = self.user_name.get()
        password = self.user_pass.get()
        user_id = load_user_session()

        Database().save_user_data(user_id, website, username, password)
        print(f"data for website: [{website}] saved")

    def generate(self):
        """Populate table and create as many rows as entries to display"""
        accounts = [
            ["example.com", "user123", "password123"],
            ["google.com", "admin@google.com", "xDeR5j-X"],
            ["amazon.co.uk", "prince", "royal_flush$$$"],
            ["test.net", "test_user1", "Long_password123"],
            ["test.net", "test_user2", "short_pass"]
        ]

        for i, account in enumerate(accounts):
            self.table.add_row(account, i + 1)
