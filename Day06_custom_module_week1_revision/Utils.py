"""
utils.py
Reusable helper functions used across multiple Python projects.
"""

# -------------------------------------------------------------------

import random
import string
from datetime import datetime

# -------------------------------------------------------------------

def generate_password(length: int = 12) -> str:
    """
    Generate a secure random password.

    Args:
        length (int): Length of the password.

    Returns:
        str: Randomly generated password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


def format_date(date_obj: datetime) -> str:
    """
    Convert datetime object to readable string format.

    Args:
        date_obj (datetime): Date object.

    Returns:
        str: Formatted date string.
    """
    return date_obj.strftime("%d-%m-%Y %H:%M:%S")


def is_even(number: int) -> bool:
    """
    Check if a number is even.

    Args:
        number (int): Number to check.

    Returns:
        bool: True if even, otherwise False.
    """
    return number % 2 == 0


def unique_list(items: list) -> list:
    """
    Remove duplicate elements from a list.

    Args:
        items (list): Input list.

    Returns:
        list: List with unique elements.
    """
    return list(set(items))

def safe_divide(a: float, b: float) -> float:
    """
    Divide two numbers safely.

    Args:
        a (float): Numerator
        b (float): Denominator

    Returns:
        float: Result of division or 0 if division by zero.
    """
    try:
        return a / b
    except ZeroDivisionError:
        return 0