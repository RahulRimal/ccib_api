import pytest

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.request import HttpRequest

from model_bakery import baker

from autho.models import User


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


@pytest.mark.django_db
class TestHasWritePermission(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.superuser = baker.make("autho.User", password=make_password("admin"), is_superuser=True)
        cls.regular_user = baker.make("autho.User", password=make_password("password"))
        cls.finance = baker.make("cooperative.Finance")
        cls.finance_staffuser = baker.make("autho.User", password=make_password("password"))
        cls.finance_staff = baker.make("cooperative.FinanceStaff", user=cls.finance_staffuser, finance=cls.finance)
        cls.active_subscription = baker.make("subscription.Subscription", finance=cls.finance, status="active")
       
    def test_with_no_request_path(self):
        request = HttpRequest()
        result = User.has_write_permission(request=request)
        self.assertFalse(result)

    def test_with_invalid_request_path(self):
        request = HttpRequest()
        request.path = "/test-path"
        result = User.has_write_permission(request=request)
        self.assertFalse(result)

    def test_for_create_token_path_with_no_request_data(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {}
        result = User.has_write_permission(request=request)
        self.assertFalse(result)

    def test_for_create_token_path_with_invalid_credentials(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {"username": "username", "password": "password"}
        result = User.has_write_permission(request=request)
        self.assertFalse(result)

    def test_for_create_token_path_with_superuser(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {"username": self.superuser.username, "password": "admin"}
        result = User.has_write_permission(request=request)
        self.assertTrue(result)
    
    def test_for_create_token_path_with_regular_user(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {"username": self.regular_user.username, "password": "password"}
        result = User.has_write_permission(request=request)
        self.assertFalse(result)

    def test_for_create_token_path_with_finance_staff_user_with_no_active_subscription(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {"username": self.finance_staffuser.username, "password": "password"}
        self.active_subscription.status = "inactive"
        self.active_subscription.save()
        result = User.has_write_permission(request=request)
        self.assertFalse(result)
    
    def test_for_create_token_path_with_finance_staff_user_with_active_subscription(self):
        request = HttpRequest()
        request.path = "/auth/create-token/"
        request.data = {"username": self.finance_staffuser.username, "password": "password"}
        result = User.has_write_permission(request=request)
        self.assertTrue(result)


    
       
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
            "/auth/users/:idx/change_password/",
            {
                "old_password": "old_password",
                "new_password": "new_password",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertTrue(self.user.check_password("new_password"))
