"""
Student registration and hostel room allocation module.
"""

from datetime import datetime


def get_non_empty(prompt):
    """
    Ask the user for information and reject empty input.
    """

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def find_room(data, room_id):
    """
    Find a hostel room using its room ID.

    Returns:
        block_name, room
    """

    room_id = room_id.upper()

    for block_name, rooms in data["rooms"].items():

        if room_id in rooms:
            return block_name, rooms[room_id]

    return None, None


def register_student(data):
    """
    Register a new student and allocate the student
    to a specified hostel room.
    """

    print("\n" + "=" * 60)
    print("STUDENT REGISTRATION AND ROOM ALLOCATION")
    print("=" * 60)

    # Get registration number
    reg_no = get_non_empty(
        "Registration number: "
    ).upper()

    # Check for duplicate registration number
    if reg_no in data["students"]:

        print(
            "A student with this registration number "
            "already exists."
        )

        return

    # Get student's name
    name = get_non_empty(
        "Student name: "
    )

    # Get programme
    program = get_non_empty(
        "Programme/Course: "
    )

    # Get hostel fee
    while True:

        try:

            total_fee = float(
                input(
                    "Total hostel fee (UGX): "
                )
            )

            if total_fee < 0:

                print(
                    "Fee cannot be negative."
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid number."
            )

    # Create student record
    student = {

        "reg_no": reg_no,

        "name": name,

        "program": program,

        "total_fee": total_fee,

        "room_id": None,

        "block": None,

        "registered_at":
            datetime.now().isoformat(
                timespec="seconds"
            )
    }

    # Store student information
    data["students"][reg_no] = student

    print(
        "\nStudent registered successfully."
    )

    # Ask for room allocation
    allocate_student(
        data,
        reg_no
    )


def allocate_student(data, reg_no):
    """
    Allocate a registered student to a hostel room.

    A student can only be allocated if the room exists
    and still has available space.
    """

    student = data["students"].get(
        reg_no
    )

    if not student:

        print(
            "Student was not found."
        )

        return False

    # Check if student already has a room
    if student["room_id"]:

        print(
            f"Student is already allocated "
            f"to room {student['room_id']}."
        )

        return False

    # Request room ID
    room_id = input(
        "\nEnter room ID "
        "(Example: A01, B03, C05): "
    ).strip().upper()

    # Find room
    block_name, room = find_room(
        data,
        room_id
    )

    # Check whether room exists
    if room is None:

        print(
            "\nALLOCATION REJECTED!"
        )

        print(
            f"Room {room_id} does not exist."
        )

        return False

    # Calculate current occupancy
    current_occupancy = len(
        room["students"]
    )

    maximum_capacity = room["capacity"]

    # Check whether room is full
    if current_occupancy >= maximum_capacity:

        print(
            "\nALLOCATION REJECTED!"
        )

        print(
            f"Room {room_id} is FULL."
        )

        print(
            f"Current occupancy: "
            f"{current_occupancy}/"
            f"{maximum_capacity}"
        )

        return False

    # Add student to room
    room["students"].append(
        reg_no
    )

    # Update student's room information
    student["room_id"] = room_id

    student["block"] = block_name

    # Calculate new occupancy
    new_occupancy = len(
        room["students"]
    )

    print(
        "\nALLOCATION SUCCESSFUL!"
    )

    print(
        f"Student: {student['name']}"
    )

    print(
        f"Block: {block_name}"
    )

    print(
        f"Room: {room_id}"
    )

    print(
        f"Occupancy: "
        f"{new_occupancy}/"
        f"{maximum_capacity}"
    )

    return True