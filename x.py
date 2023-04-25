import PySimpleGUI as sg
import json
from cryptography.fernet import Fernet

# Password dictionary
with open("database.txt", "r") as db:
    database = json.load(db)


def create_window():
    # App layout

    layout = [
        [sg.Input("website", key="-WEB-")],
        [sg.Input("password", key="-PASS-")],
        [sg.Button("Submit", key="-SUBMIT-")],
        [sg.Input("", key="-S-INPUT-")],
        [sg.Button("Search", key="-SEARCH-")],
        [sg.Text("", key="-MESSAGE-")],
        [sg.Text("", key="-MESSAGE2-")]
    ]

    return sg.Window("Password storage", layout,
                     element_justification="center",
                     size=(400, 250))


def encrypt_password(password):
    # Encrypt password entry

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encoded_password = fernet.encrypt(password.encode())
    return key, encoded_password


def decrypt_password(key, encoded_password):
    # Decrypt password entry

    fernet = Fernet(key)
    decoded_password = fernet.decrypt(encoded_password)
    return decoded_password


def password_storage():

    window = create_window()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-SUBMIT-":
            # Update database dictionary
            web = values["-WEB-"]
            pas = values["-PASS-"]
            # Encrypt passwords

            database.update({str(web): str(pas)})
            # Write dictionary to json
            with open("database.txt", "w") as db:
                json.dump(database, db)
            print(database)

        if event == "-SEARCH-":
            search_term = values["-S-INPUT-"]
            # Read json
            with open("database.txt", "r") as db:
                database = json.load(db)

            # Display searched values
            try:
                res = dict(filter(lambda item: search_term in item[0], database.items()))
                ls1 = list(res.keys())
                for key, value in database.items():
                    print(key, value)
                window["-MESSAGE-"].update(ls1)
                ls2 = list(res.values())
                window["-MESSAGE2-"].update(ls2)
            except KeyError:
                window["-MESSAGE-"].update("Doesn't exist")

    window.close()


if __name__ == "__main__":
    password_storage()
