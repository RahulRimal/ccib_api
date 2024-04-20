from django.db import models

# Create your models here.
from django.contrib.auth.models import User as BaseUser
from common.models import BaseModelMixin


class User(BaseUser, BaseModelMixin):
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    citizenship_number = models.CharField(max_length=50)
    citizenship_issued_place = models.CharField(max_length=255)
    citizenship_issued_date = models.DateField()
    dob = models.DateField(blank=True, null=True)
    fathers_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # groups = models.ManyToManyField("auth.Group", related_name="ccib_user_groups")
    # permissions = models.ManyToManyField(
    #     "auth.Permission", related_name="custom_user_permissions"
    # )

    def __str__(self):
        return self.name
