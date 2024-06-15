from django.contrib import admin

from autho.models import StaffUser, User

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


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "first_name",
        "last_name",
        "dob",
        "father_name",
        "phone_number",
        "is_staff",
    ]