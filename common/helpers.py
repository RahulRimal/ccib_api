from autho.models import User
from django.utils import timezone
from datetime import date, datetime


def generate_username(first_name: str, last_name: str) -> str:
    """Generate a unique username"""
    username = first_name + last_name
    if User.objects.filter(username=username).exists():
        username = username + str(User.objects.count() + 1)
    return username


def get_local_datetime() -> datetime:
    return timezone.now()


def get_local_date() -> date:
    return timezone.now().date()
