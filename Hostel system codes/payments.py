"""
Handles hostel fee payments and outstanding balances.
"""

from datetime import datetime


def get_student(data):
    """
    Find a student using registration number.
    """

    reg_no = input(
        "Student registration number: "
    ).strip().upper()

    student = data["students"].get(
        reg_no
    )

    if not student:

        print(
            "Student not found."
        )

        return None

    return student


def total_paid(data, reg_no):
    """
    Calculate the total amount paid
    by a particular student.
    """

    total = 0

    for payment in data["payments"]:

        if payment["reg_no"] == reg_no:

            total += payment["amount"]

    return total


def outstanding_balance(data, reg_no):
    """
    Calculate the student's outstanding hostel fee.
    """

    student = data["students"][reg_no]

    paid = total_paid(
        data,
        reg_no
    )

    balance = (
        student["total_fee"] - paid
    )

    # Do not allow negative balance
    return max(
        0,
        balance
    )


def record_payment(data):
    """
    Record either a full or partial hostel fee payment.
    """

    print("\n" + "=" * 60)
    print("FEE PAYMENT RECORDING")
    print("=" * 60)

    student = get_student(
        data
    )

    if not student:
        return

    reg_no = student["reg_no"]

    # Calculate existing payments
    paid_so_far = total_paid(
        data,
        reg_no
    )

    balance = outstanding_balance(
        data,
        reg_no
    )

    print(
        f"\nStudent: {student['name']}"
    )

    print(
        f"Registration: {student['reg_no']}"
    )

    print(
        f"Total hostel fee: "
        f"UGX {student['total_fee']:,.0f}"
    )

    print(
        f"Paid so far: "
        f"UGX {paid_so_far:,.0f}"
    )

    print(
        f"Outstanding balance: "
        f"UGX {balance:,.0f}"
    )

    # No payment required
    if balance == 0:

        print(
            "\nThis student has already "
            "cleared the hostel fee."
        )

        return

    # Enter payment amount
    while True:

        try:

            amount = float(
                input(
                    "\nPayment amount (UGX): "
                )
            )

            if amount <= 0:

                print(
                    "Payment must be greater than zero."
                )

                continue

            if amount > balance:

                print(
                    f"Payment rejected."
                )

                print(
                    f"Maximum allowed payment: "
                    f"UGX {balance:,.0f}"
                )

                continue

            break

        except ValueError:

            print(
                "Please enter a valid amount."
            )

    reference = input(
        "Payment reference "
        "(optional): "
    ).strip()

    # Create payment record
    payment = {

        "reg_no": reg_no,

        "amount": amount,

        "reference": reference,

        "date":
            datetime.now().isoformat(
                timespec="seconds"
            )
    }

    # Store payment
    data["payments"].append(
        payment
    )

    # Calculate new balance
    new_balance = outstanding_balance(
        data,
        reg_no
    )

    print("\nPAYMENT RECORDED SUCCESSFULLY!")

    print(
        f"Amount paid: "
        f"UGX {amount:,.0f}"
    )

    print(
        f"New outstanding balance: "
        f"UGX {new_balance:,.0f}"
    )