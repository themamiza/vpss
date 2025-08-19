#!/usr/bin/env python3

from user import add_user, validate_username, user_exists, remove_user, set_max_connections, set_user_expiry, resurrect_users
from utils import validate_and_format_fixed_date, calc_relative_expiry_date, clear_screen
from live_monitor import live_monitor

def print_menu() -> None:
    print("""
===== VPS User Management =====

1) Add user
2) Remove user
3) Change user expiry
4) Change user max connections
5) Live monitor
6) Resurrect users
0) Exit (Ctrl-C at any point to exit)

""")

def handle_add_user() -> None:
    username = input("Enter new username: ")

    if not validate_username(username):
        print(f"'{username}' is not a valid username.")
        exit(1)
 
    if user_exists(username):
        print(f"'{username}' already exists on the system.")
        exit(1)

    print("""
Set expiry date

    1) Fixed date (YYYY-MM-DD)
    2) Relative (+days)
""")

    choice = input("How are you going to provide exipry date (1/2)? ")

    print()

    # Fixed date
    if choice == "1":
        date_str = input("Enter expiry date (YYYY-MM-DD): ")
        try:
            expiry = validate_and_format_fixed_date(date_str)
        except ValueError as e:
            print(f"Error {e}")
            exit(1)
    # Relative
    elif choice == "2":
        try:
            days = int(input("Enter number of days from today: "))
            expiry = calc_relative_expiry_date(days)
        except ValueError:
            print("Invalid number of days.")
            exit(1)
    else:
        print("Invalid choice.")
        exit(1)

    print()

    try:
        max_connections = int(input("Enter max connections: "))
    except ValueError:
        print("Invalid number.")
        exit(1)

    try:
        password = add_user(username=username, expiry=expiry, max_connections=max_connections)
        print(f"""
    User '{username}' added successfully!
    Password: {password}
    Expires: {expiry}
    Max connections: {max_connections}
""")
    except Exception as e:
        print(f"[!] Failed to add user '{username}': {e}")
        exit(1)

def handle_remove_user() -> None:
    username = input("Enter username to remove: ")

    if not validate_username(username):
        print(f"'{username}' is not a valid username.")
        exit(1)
 
    if not user_exists(username):
        print(f"'{username}' does not exist on the system.")
        exit(1)

    try:
        remove_user(username)
    except:
        print(f"Could not remove '{username}'.")
        exit(1)

    print(f"'{username}' removed successfully.")

def handle_change_exipry() -> None:
    username = input("Enter username to change expiry date: ")

    print("Set expiry date\n\n\t1) Fixed date (YYYY-MM-DD)\n\t2) Relative (+days)\n\t3) Relative from user's expiry\n")

    choice = input("How are you going to provide exipry date (1-3)? ")

    if choice == "1":
        date_str = input("Enter expiry date (YYYY-MM-DD): ")
        try:
            expiry = validate_and_format_fixed_date(date_str)
        except ValueError as e:
            print(f"Error {e}")
            return
    elif choice == "2":
        try:
            days = int(input("Enter number of days from today: "))
            expiry = calc_relative_expiry_date(days)
        except ValueError:
            print("Invalid number of days.")
            return
    elif choice == "3":
        raise NotImplementedError
    else:
        print("Invalid choice.")
        return

    set_user_expiry(username, expiry)   

def handle_change_max_connections() -> None:
    username = input("Enter new username: ")

    if not validate_username(username):
        print(f"'{username}' is not a valid username.")
        exit(1)
 
    if not user_exists(username):
        print(f"'{username}' does not exist on the system.")
        exit(1)

    try:
        max_connections = int(input("Enter new max connections: "))
    except ValueError:
        print("Invalid number")

    set_max_connections(username, max_connections)

def handle_resurrect_users() -> None:
    print("== Resurrect users ==")
    summary = resurrect_users()
    print("\nSummary:")
    print(f"  created: {summary.get('created', [])}")
    print(f"  updated: {summary.get('updated', [])}")
    print(f"  errors : {summary.get('errors', [])}")
    input("\nPress Enter to continue...")

def main() -> None:
    try:
        clear_screen()
        print_menu()

        """
            1) Add user
            2) Remove user
            3) Change user expiry
            4) Change user max connections
            5) Live monitor
            0) Exit (Ctrl-C at any point to exit)
        """

        choice = input("Choose an action: ")

        clear_screen()

        if choice == "0":
            exit(0)
        elif choice == "1":
            handle_add_user()
        elif choice == "2":
            handle_remove_user()
        elif choice == "3":
            handle_change_exipry()
        elif choice == "4":
            handle_change_max_connections()
        elif choice == "5":
            live_monitor()
        elif choice == "6":
            handle_resurrect_users()

        print()

    except KeyboardInterrupt:
        print("\n")
        exit(130)

if __name__ == "__main__":
    main()
