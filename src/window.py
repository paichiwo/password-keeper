import customtkinter as ctk


class PasswordKeeper(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.iconbitmap("./img/icon_512x512.ico")
        self.title("Password Keeper")
        self.geometry("450x450")

        self.user_name = None

        self.root_label = ctk.CTkLabel(self, text="LOGO")
        self.root_label.pack(padx=10, pady=10)

        self.password_keeper_frame()

    def password_keeper_frame(self):

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.user_name = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.user_name.pack(padx=10, pady=20)

