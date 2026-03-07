"""
utils/data_generator.py

Provides helper functions for generating dynamic test data at runtime.
"""

import random

def generate_random_postal_code() -> str:
    """
    Generates a random 6-digit postal code string, as required by the checkout
    information step. Pads with leading zeros if necessary to ensure exactly 6 digits.

    Returns:
        str: A 6-digit numeric string (e.g., "042918")
    """
    return f"{random.randint(0, 999999):06d}"

