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
    """ Application layout and theme """

    psg.theme("DarkTeal2")

    layout = [
        [psg.Text("username / website")], [psg.Input("", key="-USERNAME-")],
        [psg.Text("password")], [psg.Input("", key="-PASSWORD-")],
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


def add_password(web, pas, database, db_file_path):
    """ Add password to the database """
    # Encrypt passwords
    key, encoded_password = encrypt_password(pas)
    database.update({str(web): [key.decode(), encoded_password.decode()]})

    # Write dictionary as json
    with open(db_file_path, "w") as db:
        json.dump(database, db)


def search_database(search_term, db_file_path):
    """ Search for entries in the database file """

    # Read the database
    with open(db_file_path, "r") as db:
        database = json.load(db)

    # Display searched values
    result = {key: value for key, value in database.items() if search_term in key}
    list_1 = list(result.keys())
    list_2 = []
    for key, value in result.items():
        key = value[0].encode()
        encoded_password = value[1].encode()
        list_2.append(decrypt_password(key, encoded_password).decode())
    return list_1, list_2


def password_keeper(database):

    window = create_window()

    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break

        if event == "-GENERATE-":
            # Display generated password
            password = generate_password()
            window["-PASSWORD-"].update(password)

        if event == "-SUBMIT-":
            # Add password to the database
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]
            add_password(username, password, database, "database.txt")
            window["-USERNAME-"].update("")
            window["-PASSWORD-"].update("")

        if event == "-SEARCH-":
            # Search for passwords
            search_term = values["-SEARCH-INPUT-"]
            ls1, ls2 = search_database(search_term, "database.txt")
            if len(ls1) == 0 and len(ls2) == 0:
                window["-MESSAGE1-"].update("Doesn't exist")
                window["-MESSAGE2-"].update("")
            else:
                window["-MESSAGE1-"].update(ls1)
                window["-MESSAGE2-"].update(ls2)

    window.close()
    return database


def main():
    """ Application flow """
    try:
        with open("database.txt", "r") as db:
            database = json.load(db)
    except (ValueError, FileNotFoundError):
        database = {}

    database = password_keeper(database)

    with open("database.txt", "w") as db:
        json.dump(database, db)


if __name__ == "__main__":
    main()
