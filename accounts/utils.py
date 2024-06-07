import random
import re
from django.core.mail import EmailMultiAlternatives
from django.forms import ValidationError



def otp_generation():
    """
    Generate a 6-digit OTP (One-Time Password).

    This function generates a random 6-digit number which can be used as an OTP
    for authentication purposes.

    Returns:
        int: A 6-digit random integer between 100000 and 999999.
    """
    return random.randint(100000, 999999)


def validate_password(value):
    if len(value) < 8:
        raise ValidationError(
            "Password must be at least 8 characters long")
    if not any(char.islower() for char in value):
        raise ValidationError(
            "Password must contain at least one lowercase letter")
    if not any(char.isupper() for char in value):
        raise ValidationError(
            "Password must contain at least one uppercase letter")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(
            "Password must contain at least one special character")
    return True