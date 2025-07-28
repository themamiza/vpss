#!/usr/bin/env python3

from time import sleep
from utils import days_remaining, clear_screen
from user import load_users, USERS_FILE, get_user_expiry
from ssh_control import count_connections, kill_excess_connections

def live_monitor() -> None:
    try:
        while True:
            clear_screen()
            print("=== Live SSH User Monitor ===\n")
            users = load_users()
            if not users:
                print(f"No user found in '{USERS_FILE}'")
            else:
                for user in users:
                    username = user["username"]
                    expiry = user["expiry"]
                    max_connections = user["max_connections"]

                    connection_count = count_connections(username)
                    maxed_mark = "*" if max_connections == connection_count else " "

                    if connection_count > count_connections:
                        kill_excess_connections(username, max_connections)

                    if get_user_expiry(username) == "never":
                        days_left = ""
                    else:
                        days_left = str(days_remaining(get_user_expiry(username))) + " " + "days left"

                    print(f"[{connection_count}]{maxed_mark}\t\t{username}\t\t{days_left}")
            print()
            print("Press Ctrl+c to stop.")
            sleep(1)
    except KeyboardInterrupt:
        print("\nExiting live monitor.")

if __name__ == "__main__":
    live_monitor()
