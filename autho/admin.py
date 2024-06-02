from django.contrib import admin

from autho.models import User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "first_name",
        "last_name",
        "dob",
        "father_name",
        "phone_number",
    ]
