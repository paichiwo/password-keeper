#!/usr/bin/env python3

"""
The Password Keeper application creates powerful passwords,
encodes them, and securely stores them all in one convenient location
"""

import PySimpleGUI as psg
import json
import random
import string
from cryptography.fernet import Fernet


def create_window():
    # App layout

    psg.theme("DarkTeal2")

    layout = [
        [psg.Text("username / website")], [psg.Input("", key="-WEB-")],
        [psg.Text("password")], [psg.Input("", key="-PASS-")],
        [psg.Button("Generate", key="-GENERATE-"), psg.Button("Submit", key="-SUBMIT-")],
        [psg.Text("")],
        [psg.Input("", key="-SEARCH-INPUT-")],
        [psg.Button("Search", key="-SEARCH-")],
        [psg.Text("", key="-MESSAGE1-")],
        [psg.Text("", key="-MESSAGE2-")]
    ]
    return psg.Window("password-keeper", layout, resizable=True,
                      element_justification="center",
                      size=(400, 280))


def encrypt_password(password):
    """ Encrypt password entry """

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encoded_password = fernet.encrypt(password.encode())
    return key, encoded_password


def decrypt_password(key, encoded_password):
    """ Decrypt password entry """

    fernet = Fernet(key)
    decoded_password = fernet.decrypt(encoded_password)
    return decoded_password


def generate_password():
    """ Generate passwords between 14 and 20 characters long using letters, numbers and symbols"""

    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    length = random.randrange(14, 21)
    password = ""
    for character in range(length):
        password += random.choice(characters)
    return password


def password_storage(database):

    window = create_window()

    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break

        if event == "-GENERATE-":
            # Display generated password
            password = generate_password()
            window["-PASS-"].update(password)

        if event == "-SUBMIT-":
            # Update database dictionary
            web = values["-WEB-"]
            pas = values["-PASS-"]
            # Clear entry data
            window["-WEB-"].update("")
            window["-PASS-"].update("")
            # Encrypt passwords
            key, encoded_password = encrypt_password(pas)
            database.update({str(web): [key.decode(), encoded_password.decode()]})
            # Write dictionary to json
            with open("database.txt", "w") as db:
                json.dump(database, db)
            print(database)

        if event == "-SEARCH-":
            search_term = values["-SEARCH-INPUT-"]
            # Read json
            with open("database.txt", "r") as db:
                database = json.load(db)
            # Display searched values
            res = dict(filter(lambda item: search_term in item[0], database.items()))
            ls1 = list(res.keys())
            window["-MESSAGE1-"].update(ls1)
            ls2 = []
            for key, value in res.items():
                key = value[0].encode()
                encoded_password = value[1].encode()
                ls2.append(decrypt_password(key, encoded_password).decode())
            window["-MESSAGE2-"].update(ls2)
            # If search term cannot be found
            if len(ls1) == 0 and len(ls2) == 0:
                window["-MESSAGE1-"].update("Doesn't exist")
                window["-MESSAGE2-"].update("")

    window.close()
    return database


def main():
    """ Main function """
    try:
        with open("database.txt", "r") as db:
            database = json.load(db)
    except (ValueError, FileNotFoundError):
        database = {}

    database = password_storage(database)

    with open("database.txt", "w") as db:
        json.dump(database, db)


if __name__ == "__main__":
    main()
