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
        "dob",
        "father_name",
        "phone_number",
        "is_active",
        "is_staff"
    ]
