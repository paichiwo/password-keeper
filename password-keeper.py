#!/usr/bin/env python3

"""
The Password Keeper application creates powerful passwords,
encodes them, and securely stores them all in one convenient location
"""

import PySimpleGUI as psg
import json
import random
import string
from itertools import islice
from cryptography.fernet import Fernet


def create_window():
    """Application layout and theme"""

    psg.theme("DarkTeal2")

    layout = [
        [psg.Text("Username / Website:")], [psg.Input("", key="-USERNAME-")],
        [psg.Text("Password:")], [psg.Input("", key="-PASSWORD-")],
        [psg.Button("Generate", key="-GENERATE-", size=7), psg.Button("Submit", key="-SUBMIT-", size=7)],
        [psg.Text("Search:")],
        [psg.Input("", key="-SEARCH-INPUT-")],
        [psg.Button("Search", key="-SEARCH-", size=7), psg.Button("Delete", key="-DELETE-", disabled=True, size=7)],
        [psg.Table(values=[], headings=["Username / Website", "Password"],
                   key="-TABLE-",
                   auto_size_columns=True,
                   justification="left",
                   selected_row_colors="black on grey",
                   enable_events=True,
                   expand_x=True,
                   expand_y=True
                   )]
    ]
    return psg.Window("password-keeper", layout, resizable=True,
                      element_justification="center",
                      size=(450, 450))


def encrypt_password(password):
    """Encrypt password"""

    key = Fernet.generate_key()
    fernet = Fernet(key)
    encoded_password = fernet.encrypt(password.encode())
    return key, encoded_password


def decrypt_password(key, encoded_password):
    """Decrypt password"""

    fernet = Fernet(key)
    decoded_password = fernet.decrypt(encoded_password)
    return decoded_password


def generate_password():
    """Generate passwords between 14 and 20 characters long using letters, numbers and symbols"""

    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    length = random.randrange(14, 21)
    password = ""
    for character in range(length):
        password += random.choice(characters)
    return password


def add_password(web, pas, database, db_file_path):
    """Add password to the database"""

    # Encrypt passwords
    key, encoded_password = encrypt_password(pas)
    database.update({str(web): [key.decode(), encoded_password.decode()]})

    # Update the database file
    with open(db_file_path, "w") as db:
        json.dump(database, db)


def search_database(search_term, db_file_path):
    """Search for entries in the database file"""

    # Read the database
    with open(db_file_path, "r") as db:
        database = json.load(db)

    # Display searched values
    result = {key: value for key, value in database.items() if search_term in key}
    return result


def update_table(window, data):
    """Update table with the search results"""

    table = window["-TABLE-"]
    table.update(visible=True)
    table_values = [
        [key, decrypt_password(value[0].encode(), value[1].encode()).decode()] for key, value in data.items()
    ]
    table.update(values=table_values)


def delete_row(selected_row, database, db_file_path):
    """Delete selected row from the database"""

    key = selected_row[0]
    del database[next(islice(database, key, None))]

    # Update the database file
    with open(db_file_path, "w") as db:
        json.dump(database, db)


def password_keeper(database):
    """
    This function creates a PySimpleGUI window and listens for events to perform various actions
    Parameters:   database (dict): a dictionary object representing the password database

    - Generate a random password when the "Generate" button is clicked
    - Add a new username and password to the database when the "Submit" button is clicked
    - Search the database for passwords that match a search term when the "Search" button is clicked
    - Delete the selected row from the database when the "Delete" button is clicked

    Returns:   database (dict): the updated password database after the user closes the window
    """
    window = create_window()

    while True:
        event, values = window.read()
        if event == psg.WIN_CLOSED:
            break

        # Display generated password
        if event == "-GENERATE-":
            password = generate_password()
            window["-PASSWORD-"].update(password)

        # Add password to the database
        if event == "-SUBMIT-":
            username = values["-USERNAME-"]
            password = values["-PASSWORD-"]
            if not username or not password:
                psg.popup("Please fill in the Username and Password fields.", title="Submit")
            else:
                add_password(username, password, database, "database.txt")
                window["-USERNAME-"].update("")
                window["-PASSWORD-"].update("")

        # Search for passwords
        if event == "-SEARCH-":
            search_term = values["-SEARCH-INPUT-"]
            data = search_database(search_term, "database.txt")
            if data:
                update_table(window, data)
                window["-DELETE-"].update(disabled=False)
            else:
                psg.popup("Search Error, item doesn't exist.", title="Search")

        # Delete the selected row from the database and update the table
        if event == "-DELETE-":
            selected_row = values["-TABLE-"]
            delete_row(selected_row, database, "database.txt")
            data = search_database(values["-SEARCH-INPUT-"], "database.txt")
            if data:
                update_table(window, data)

    window.close()
    return database


def main():
    """Main function that loads the database, calls the password_keeper function,
    and saves the updated database to a file"""
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
