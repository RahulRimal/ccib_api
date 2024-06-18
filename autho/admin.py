from django.contrib import admin

from autho.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "first_name",
        "last_name",
    ]
 