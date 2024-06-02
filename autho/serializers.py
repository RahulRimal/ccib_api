from django.db import IntegrityError
from rest_framework import serializers
from autho.models import StaffUser, User
from common.helpers import generate_username
from common.mixins import BaseModelSerializerMixin


class UserSerializer(BaseModelSerializerMixin):

    class Meta:
        model = User
        fields = [
            "idx",
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "dob",
            "father_name",
            "mother_name",
            "grandfather_name",
            "phone_number",
            "gender",
            "permanent_address",
            "temporary_address",
        ]

    # def create(self, validated_data):
    #     username = generate_username(
    #         validated_data["first_name"], validated_data["last_name"]
    #     )
    #     validated_data["username"] = username
    #     return super().create(validated_data)

    # def update(self, instance, validated_data):
    #  username = generate_username(
    #     validated_data.get("first_name", instance.first_name),
    #     validated_data.get("last_name", instance.last_name),
    # )
    #  validated_data["username"] = username
    #  return super().update(instance, validated_data)


class StaffUserSerializer(BaseModelSerializerMixin):

    
    class Meta:
        model = StaffUser
        fields = ["idx", "user"]
        serializers = {"user": UserSerializer}

    def create(self, validated_data):

        username = generate_username(
            validated_data["user"].first_name, validated_data["user"].last_name
        )
        validated_data["username"] = username
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        username = generate_username(
            validated_data.get("first_name", instance.first_name),
            validated_data.get("last_name", instance.last_name),
        )
        validated_data["username"] = username
        return super().update(instance, validated_data)
  