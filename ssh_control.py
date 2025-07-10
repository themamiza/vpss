#!/usr/bin/env python3

from time import sleep
import subprocess
from typing import List
from user import load_users

def get_active_ssh_connections(username: str) -> List:
    try:
        result = subprocess.run(
                ["pgrep", "-u", username, "-f", "sshd"],
                capture_output=True, text=True, check=True
        )
        pids = result.stdout.strip().split("\n")
        return [pid for pid in pids if pid]
    except subprocess.CalledProcessError:
        # pgrep exits with exit code 1 if there were not matches
        return []

def count_connections(username: str) -> int:
    return len(get_active_ssh_connections(username))

def kill_excess_connections(username: str, max_connections: int) -> None:
    pids = get_active_ssh_connections(username)
    if len(pids) > max_connections:
        number_of_excess_connections = len(pids) - max_connections

        pids_sorted = sorted(pids, key=int)
        pids_to_kill = pids_sorted[:number_of_excess_connections]

        print(f"Killing {number_of_excess_connections} old connections for {username}: {pids_to_kill}")

        for pid in pids_to_kill:
            subprocess.run(["kill", "-9", pid], check=True)

if __name__ == "__main__":
    while True:
        users = load_users()
        for user in users:
            username = user["username"]
            max_connections = user["max_connections"]
            kill_excess_connections(username, max_connections)
        sleep(2)

