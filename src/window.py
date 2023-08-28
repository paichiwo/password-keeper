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

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=20, pady=20, fill='both', expand=True, anchor='center')
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.user_name = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.user_name.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

        self.user_pass = ctk.CTkEntry(self.frame, placeholder_text="Password")
        self.user_pass.grid(row=0, column=1, padx=20, pady=20, sticky='ew')

        self.save_btn = ctk.CTkButton(self.frame, text="Save Account")
        self.save_btn.grid(row=1, column=0, padx=20, sticky='ew')

        self.generate_btn = ctk.CTkButton(self.frame, text="Generate")
        self.generate_btn.grid(row=1, column=1, padx=20, sticky='ew')
