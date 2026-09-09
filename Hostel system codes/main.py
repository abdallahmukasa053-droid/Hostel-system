"""
Hostel Room Booking and Fees Management System
Main driver program.
"""

from hostel_data import load_data, save_data, initialize_data
from registration import register_student
from payments import record_payment
from reports import (
    occupancy_overview,
    search_student,
    hostel_occupancy_report,
    fee_defaulters
)


def print_banner():
    print("\n" + "=" * 70)
    print("       HOSTEL ROOM BOOKING AND FEES MANAGEMENT SYSTEM")
    print("=" * 70)


def show_menu():
    print("\nMAIN MENU")
    print("-" * 70)
    print("1. Register student and allocate room")
    print("2. Record fee payment")
    print("3. Search student")
    print("5. Show full hostel occupancy report")
    print("6. Show fee defaulters")
    print("7. Save data")
    print("0. Exit")
    print("-" * 70)


def main():
    # Load existing data or create new data
    data = load_data()
    initialize_data(data)
    save_data(data)

    print_banner()

    print("\nCURRENT HOSTEL OCCUPANCY")
    occupancy_overview(data)

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_student(data)
            save_data(data)

        elif choice == "2":
            record_payment(data)
            save_data(data)

        elif choice == "3":
            search_student(data)

        elif choice == "4":
            occupancy_overview(data)

        elif choice == "5":
            hostel_occupancy_report(data)

        elif choice == "6":
            try:
                threshold = float(
                    input("Enter outstanding balance threshold (UGX): ")
                )

                if threshold < 0:
                    print("Threshold cannot be negative.")
                else:
                    fee_defaulters(data, threshold)

            except ValueError:
                print("Invalid amount. Please enter a number.")

        elif choice == "7":
            save_data(data)
            print("Data saved successfully.")

        elif choice == "0":
            save_data(data)
            print("All data saved successfully.")
            print("Thank you for using the system.")
            break

        else:
            print("Invalid choice. Please select an option from 0 to 7.")


if __name__ == "__main__":
    main()