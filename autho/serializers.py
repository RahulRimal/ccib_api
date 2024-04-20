from rest_framework import serializers
from autho.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "citizenship_number",
            "citizenship_issued_place",
            "citizenship_issued_date",
            "dob",
            "father_name",
            "phone_number",
        ]
