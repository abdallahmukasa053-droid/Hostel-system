"""
Search and reporting functions.
"""

from payments import (
    total_paid,
    outstanding_balance
)


def occupancy_overview(data):
    """
    Display occupancy statistics
    for all hostel blocks.
    """

    print("\n--- OCCUPANCY OVERVIEW ---")

    total_capacity = 0

    total_occupied = 0

    for block_name, rooms in data["rooms"].items():

        block_capacity = 0

        block_occupied = 0

        for room in rooms.values():

            block_capacity += room["capacity"]

            block_occupied += len(
                room["students"]
            )

        total_capacity += block_capacity

        total_occupied += block_occupied

        if block_capacity > 0:

            percentage = (
                block_occupied /
                block_capacity
            ) * 100

        else:

            percentage = 0

        print(
            f"{block_name}: "
            f"{block_occupied}/"
            f"{block_capacity} occupants "
            f"({percentage:.1f}%)"
        )

    if total_capacity > 0:

        total_percentage = (
            total_occupied /
            total_capacity
        ) * 100

    else:

        total_percentage = 0

    print("-" * 55)

    print(
        f"TOTAL: "
        f"{total_occupied}/"
        f"{total_capacity} occupants "
        f"({total_percentage:.1f}%)"
    )


def search_student(data):
    """
    Search for students by name
    or registration number.
    """

    print("\n--- SEARCH STUDENT ---")

    search_term = input(
        "Enter student name or registration number: "
    ).strip().lower()

    matches = []

    for student in data["students"].values():

        if (
            search_term in
            student["name"].lower()
            or
            search_term in
            student["reg_no"].lower()
        ):

            matches.append(
                student
            )

    if not matches:

        print(
            "\nNo matching student found."
        )

        return

    for student in matches:

        reg_no = student["reg_no"]

        paid = total_paid(
            data,
            reg_no
        )

        balance = outstanding_balance(
            data,
            reg_no
        )

        print("\n" + "-" * 60)

        print(
            f"Name: "
            f"{student['name']}"
        )

        print(
            f"Registration Number: "
            f"{student['reg_no']}"
        )

        print(
            f"Programme: "
            f"{student['program']}"
        )

        print(
            f"Hostel Block: "
            f"{student['block'] or 'Not allocated'}"
        )

        print(
            f"Room: "
            f"{student['room_id'] or 'Not allocated'}"
        )

        print(
            f"Total Hostel Fee: "
            f"UGX {student['total_fee']:,.0f}"
        )

        print(
            f"Total Paid: "
            f"UGX {paid:,.0f}"
        )

        print(
            f"Outstanding Balance: "
            f"UGX {balance:,.0f}"
        )


def hostel_occupancy_report(data):
    """
    Generate a detailed report
    for every hostel block and room.
    """

    print(
        "\n" +
        "=" * 70
    )

    print(
        "FULL HOSTEL OCCUPANCY REPORT"
    )

    print(
        "=" * 70
    )

    for block_name, rooms in data["rooms"].items():

        print(
            f"\n{block_name}"
        )

        print(
            "-" * 60
        )

        for room_id, room in rooms.items():

            occupied = len(
                room["students"]
            )

            capacity = room["capacity"]

            print(
                f"\nRoom {room_id}: "
                f"{occupied}/{capacity} occupants"
            )

            if occupied == 0:

                print(
                    "    - Empty"
                )

            else:

                for reg_no in room["students"]:

                    student = data[
                        "students"
                    ].get(reg_no)

                    if student:

                        print(
                            f"    - "
                            f"{student['name']} "
                            f"({reg_no})"
                        )


def fee_defaulters(data, threshold):
    """
    Display students whose outstanding
    balance is above the specified threshold.
    """

    print("\n" + "=" * 70)

    print(
        "FEE DEFAULTERS"
    )

    print(
        f"Students with outstanding balance "
        f"above UGX {threshold:,.0f}"
    )

    print("=" * 70)

    defaulters = []

    for student in data["students"].values():

        balance = outstanding_balance(
            data,
            student["reg_no"]
        )

        if balance > threshold:

            defaulters.append(
                (student, balance)
            )

    if not defaulters:

        print(
            "\nNo students meet the "
            "selected default threshold."
        )

        return

    # Highest outstanding balance first
    defaulters.sort(
        key=lambda item: item[1],
        reverse=True
    )

    for student, balance in defaulters:

        print(
            f"\nRegistration: "
            f"{student['reg_no']}"
        )

        print(
            f"Name: "
            f"{student['name']}"
        )

        print(
            f"Room: "
            f"{student['room_id'] or 'Not allocated'}"
        )

        print(
            f"Outstanding: "
            f"UGX {balance:,.0f}"
        )

        print("-" * 50)

    print(
        f"\nTotal number of defaulters: "
        f"{len(defaulters)}"
    )