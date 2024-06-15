from pyexpat import model
from typing import Any, Dict, Optional, Type, TypeVar

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError

from rest_framework import serializers, exceptions

from rest_framework_simplejwt.tokens import Token, RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings

from autho.models import StaffUser, User
from common.helpers import generate_username
from common.mixins import BaseModelSerializerMixin


class TokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    class Meta:
        model = StaffUser
        
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


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
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = StaffUser
        fields = [
            "idx",
            "username",
            "password",
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
          

    def create(self, validated_data):
        username = generate_username(
            validated_data["first_name"], validated_data["last_name"]
        )
        validated_data["username"] = username
        validated_data["is_staff"] = True
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        username = generate_username(
            validated_data.get("first_name", instance.first_name),
            validated_data.get("last_name", instance.last_name),
        )
        validated_data["username"] = username
        return super().update(instance, validated_data)
