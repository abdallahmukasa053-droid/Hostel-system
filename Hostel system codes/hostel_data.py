"""
Handles hostel data structures and file persistence.
"""

import json
import os
from datetime import datetime


DATA_FILE = "hostel_data.json"


def default_rooms():
    """
    Create three hostel blocks.
    Each block contains five rooms.
    Each room has a maximum capacity of four students.
    """

    blocks = {}

    for block_name in ["Block A", "Block B", "Block C"]:

        blocks[block_name] = {}

        for room_number in range(1, 6):

            room_id = f"{block_name[-1]}{room_number:02d}"

            blocks[block_name][room_id] = {
                "capacity": 4,
                "students": []
            }

    return blocks


def empty_data():
    """
    Create an empty database structure.
    """

    return {
        "rooms": default_rooms(),
        "students": {},
        "payments": []
    }


def initialize_data(data):
    """
    Make sure all required sections exist.
    """

    if "rooms" not in data:
        data["rooms"] = default_rooms()

    if "students" not in data:
        data["students"] = {}

    if "payments" not in data:
        data["payments"] = []


def load_data():
    """
    Load records from the JSON file.

    If the file does not exist, a new database is created.

    If the file is damaged, the system starts with a fresh database
    instead of crashing.
    """

    if not os.path.exists(DATA_FILE):

        print("No existing data file found.")
        print("Starting with a new hostel database.")

        return empty_data()

    try:

        with open(DATA_FILE, "r", encoding="utf-8") as file:

            data = json.load(file)

        initialize_data(data)

        print("Existing hostel data loaded successfully.")

        return data

    except (json.JSONDecodeError, OSError) as error:

        print("\nWARNING!")
        print("The hostel data file could not be read.")
        print("Reason:", error)

        print("The system will start with a fresh database.")

        # Try to preserve the damaged file
        try:

            backup_file = DATA_FILE + ".damaged"

            os.replace(DATA_FILE, backup_file)

            print(
                f"The damaged file has been preserved as "
                f"{backup_file}"
            )

        except OSError:
            pass

        return empty_data()


def save_data(data):
    """
    Save students, rooms and payment records to JSON.
    """

    data["last_saved"] = datetime.now().isoformat(
        timespec="seconds"
    )

    temporary_file = DATA_FILE + ".tmp"

    try:

        with open(
            temporary_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        os.replace(
            temporary_file,
            DATA_FILE
        )

    except OSError as error:

        print(
            "Error saving data:",
            error
        )