#!/usr/bin/env python3

import re
import os
import json
import subprocess
from typing import List, Dict
from datetime import datetime
from utils import generate_password, today_date, get_executable_path

USERS_FILE = "users.json"

def load_users() -> List[Dict]:
    if not os.path.exists(USERS_FILE):
        return []

    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users: List[Dict]) -> None:
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=8)

# Define valid username here
valid_username_regex = r'^[a-z][a-z0-9_-]{0,31}$'

def validate_username(username: str) -> bool:
    return bool(re.fullmatch(valid_username_regex, username))

def user_exists(username: str) -> bool:
    # 'not' because return code 0 means success
    return not bool(subprocess.run(["id", username], capture_output=True).returncode)

def add_user(username: str, shell: str = get_executable_path("nologin") , expiry: str = today_date(), max_connections: int = 1) -> str:
    if not validate_username(username):
        raise ValueError(f"'{username}' is not a valid username.")

    if user_exists(username):
        raise ValueError(f"'{username}' already exists on the system.")

    password = generate_password()

    subprocess.run([
        "useradd",
        "-M",
        "-s", shell,
        "-e", expiry,
        username
    ], check=True)

    subprocess.run("chpasswd", input=f"{username}:{password}".encode(), check=True)

    users = load_users()
    users.append({
        "username": username,
        "password": password,
        "expiry": expiry,
        "max_connections": max_connections
    })
    save_users(users)

    return password

def remove_user(username: str) -> None:
    if not validate_username(username):
        raise ValueError(f"'{username}' is not a valid username.")

    if not user_exists(username):
        raise ValueError(f"'{username}' does not exist on the system.")

    subprocess.run(["killall", "-q", "-u", username], capture_output=True)

    subprocess.run(["userdel", "-rf", username], check=True, capture_output=True)

    users = load_users()
    users = [u for u in users if u["username"] != username]
    save_users(users)

def set_max_connections(username: str, max_connections: int) -> None:
    users = load_users()
    done = False
    for user in users:
        if user["username"] == username:
            user["max_connections"] = max_connections
            done = True
            break
    
    if not done:
        raise ValueError(f"'{username}' not found in '{USERS_FILE}'.")
    save_users(users)

def get_user_expiry(username: str):
    if not validate_username(username):
        raise ValueError(f"'{username}' is not a valid username.")

    if not user_exists(username):
        raise ValueError(f"'{username}' does not exist on the system.")

    chage_output = subprocess.run(["chage", "-l", username], capture_output=True, check=True, text=True).stdout.splitlines()
    
    for line in chage_output:
        if "Account expires" in line:
            expiry_str = line.split(":", 1)[-1].strip()

    if expiry_str == "never":
        return expiry_str

    parsed_expiry_str = datetime.strptime(expiry_str, "%b %d, %Y")
    return parsed_expiry_str.strftime("%Y-%m-%d")

