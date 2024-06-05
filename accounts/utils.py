import random
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def otp_generation():
    """
    Generate a 6-digit OTP (One-Time Password).

    This function generates a random 6-digit number which can be used as an OTP
    for authentication purposes.

    Returns:
        int: A 6-digit random integer between 100000 and 999999.
    """
    return random.randint(100000, 999999)