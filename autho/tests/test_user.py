import pytest

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


class TestUser(TestCase):
    pass


class TestGetFullName(TestCase):
    def setUpTest(self):
        pass

    @pytest.mark.django_db
    def test_get_full_name(self):
        user = baker.make("autho.User", first_name="a", last_name="b")
        name = user.get_full_name()
        self.assertEqual(name, f"{user.first_name} {user.last_name}")


class TestGetShortName(TestCase):
    def setUpTest(self):
        pass

    @pytest.mark.django_db
    def test_get_short_name(self):
        user = baker.make("autho.User", first_name="a", last_name="b")
        name = user.get_short_name()
        self.assertEqual(name, user.first_name)
        
class TestMe(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")

    def test_me_when_user_exists(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            "/auth/users/me/",
            
        )
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    

class TestChangePassword(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User", password=make_password("old_password"))

    def test_change_password_when_user_exists(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/auth/staffusers/change_password/",
            {
                "old_password": "old_password",
                "new_password": "new_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertTrue(self.user.check_password("new_password"))
