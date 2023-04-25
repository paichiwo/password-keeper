import PySimpleGUI as sg
import json
from cryptography.fernet import Fernet


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


def password_storage(database):

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
            key, encoded_password = encrypt_password(pas)
            database.update({str(web): [key.decode(), encoded_password.decode()]})

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
                window["-MESSAGE-"].update(ls1)
                ls2 = []
                for key, value in res.items():
                    key = value[0].encode()
                    encoded_password = value[1].encode()
                    ls2.append(decrypt_password(key, encoded_password).decode())
                window["-MESSAGE2-"].update(ls2)
            except KeyError:
                window["-MESSAGE-"].update("Doesn't exist")

    window.close()
    return database


def main():

    try:
        with open("database.txt", "r") as db:
            database = json.load(db)
    except ValueError:
        database = {}

    database = password_storage(database)

    with open("database.txt", "w") as db:
        json.dump(database, db)


if __name__ == "__main__":
    main()
