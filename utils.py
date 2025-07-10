#!/usr/bin/env python3

### Imports

# Required for generating secure passwords
import secrets

# Required for character sets
import string

# Required for running system commands
import subprocess

# Required for date manipulation
from datetime import datetime, timedelta

### Variables

# Default password generation variables
password_length = 16
character_set = string.ascii_letters + string.digits

### Modules 

def generate_password(length: int = password_length, charset: str = character_set) -> str:
    """
    :param password_length: Length of the returned string.
    :param charset: Character set to make the string from.
    :return: A randomly generated string (password).
    """
    return ''.join(secrets.choice(charset) for _ in range(length))

def calc_relative_expiry_date(days_from_now: int) -> str:
    """
    :param days_from_now: Number of days from now.
    :return: Formated date string (YYYY-MM-DD) of the represented 'days_from_now'.
    """
    expiry_date = datetime.now() + timedelta(days=days_from_now)
    return expiry_date.strftime("%Y-%m-%d")

def validate_and_format_fixed_date(date_str: str) -> str:
    """
    :param date_str: Date string in (YYYY-MM-DD) format.
    :return: 'date_str' if valid, raises 'ValueError' if invalid.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

def today_date() -> str:
    """ :return: Today's date as string (YYYY-MM-DD). """
    return datetime.now().strftime("%Y-%m-%d")

def get_executable_path(executable: str) -> str:
    """
    :param executable: String representing an executable.
    :return: Executable's absolute path.
    """
    try:
        return str(subprocess.run(["whereis", executable], capture_output=True).stdout.split()[1], "utf-8")
    except IndexError:
        raise FileNotFoundError(f"'{executable}' not found.")

def days_remaining(expiry_date: str) -> int:
    """
    TODO: Complete docstring and refine function.
    """
    today = datetime.now().date()
    try:
        expiry_str = validate_and_format_fixed_date(expiry_date)
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d").date()
    except ValueError:
        return 0

    return (expiry - today).days

def clear_screen() -> None:
    try:
        subprocess.run(["clear", "-x"], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return

