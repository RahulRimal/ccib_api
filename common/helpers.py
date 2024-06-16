from django.utils import timezone
from datetime import date, datetime


def generate_username(first_name: str, last_name: str) -> str:
    """Generate a unique username"""
    
    from autho.models import User
    username = first_name + last_name
    if User.objects.filter(username=username).exists():
        username = username + str(User.objects.count() + 1)
    return username


def generate_random_number(length: int = 15) -> int:
    """Generate a random number"""
    import random
    import string
    return int("".join(random.choices(string.digits, k=length)))

def get_local_datetime() -> datetime:
    return timezone.now()


def get_local_date() -> date:
    return timezone.now().date()
