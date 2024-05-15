from django.contrib import admin

from autho.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "username",
        "first_name",
        "last_name",
        "citizenship_number",
        "citizenship_issued_place",
        "citizenship_issued_date",
        "dob",
        "fathers_name",
        "phone_number",
    ]
