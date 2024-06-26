from django.db import IntegrityError
from rest_framework import serializers
from autho.models import User
from common.helpers import generate_username
from common.mixins import BaseModelSerializerMixin


class UserSerializer(BaseModelSerializerMixin):
    username = serializers.ReadOnlyField()
    class Meta:
        model = User
        fields = [
            "idx",
            "username",
            "first_name",
            "middle_name",
            "last_name",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "dob",
            "fathers_name",
            "phone_number",
        ]

    def create(self, validated_data):
        username = generate_username(validated_data["first_name"], validated_data["last_name"]) 
        validated_data["username"] = username
        return super().create(validated_data)
