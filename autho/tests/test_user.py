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

@pytest.mark.django_db
class TestCreateUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")

    def test_user_create_when_user_exists(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "citizenship_number": self.user.citizenship_number,
                "citizenship_issued_place": self.user.citizenship_issued_place,
                "citizenship_issued_date": self.user.citizenship_issued_date,
                "father_name": self.user.father_name,
                "mother_name": self.user.mother_name,
                "grandfather_name": self.user.grandfather_name,
                "gender": self.user.gender,
                "email": self.user.email,
                "permanent_address": self.user.permanent_address,
                "temporary_address": self.user.temporary_address,

            },
        )
        self.assertEqual (response.status_code , status.HTTP_201_CREATED)

    def test_user_create_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
               "first_name":"a",
               "last_name":"b",
               "citizenship_number":"123456789",
               "citizenship_issued_place":"a",
               "citizenship_issued_date":"2020-01-01",
               "father_name":"a",
               "mother_name":"a",
               "grandfather_name":"a",
               "gender":"male",
               "email":"a@a.com",
               "permanent_address":"a",
               "temporary_address":"a",

            },
        )
        self.assertEqual (response.status_code , status.HTTP_201_CREATED)
    
    def test_user_create_when_user_already_exists(self):
        client = APIClient()
        response = client.post(
            "/auth/users/",
            {
               "first_name":"a",
               "last_name":"b",
               "citizenship_number":"123456789",
               "citizenship_issued_place":"a",
               "citizenship_issued_date":"2020-01-01",
               "father_name":"a",
               "mother_name":"a",
               "grandfather_name":"a",
               "gender":"male",
               "email":"a@a.com",
               "permanent_address":"a",
               "temporary_address":"a",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
   

@pytest.mark.django_db
class TestUpdateUser(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")

    def test_user_update_when_user_exists(self):
        client = APIClient()
        response = client.patch(
            f"/auth/users/{self.user.idx}/",
            {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            
            },
        )
        self.assertEqual(response.status_code , status.HTTP_200_OK)

    def test_user_update_when_user_does_not_exist(self):
        client = APIClient()
        response = client.patch(
            f"/auth/users/{self.user}/",
            {
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            
            },
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteUser(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")

    def test_user_delete_when_user_exists(self):
        client = APIClient()
        response = client.delete(
            f"/auth/users/{self.user.idx}/",
        )
        self.assertEqual (response.status_code , status.HTTP_204_NO_CONTENT)

    
    def test_user_delete_when_user_does_not_exist(self):
        client = APIClient()
        response = client.delete(
            f"/auth/users/{self.user}/",
        )
        self.assertEqual(response.status_code ,status.HTTP_404_NOT_FOUND)

@pytest.mark.django_db
class TestDetailUser(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")

    def test_user_detail_when_user_exists(self):
        client = APIClient()
        response = client.get(
            f"/auth/users/{self.user.idx}/",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_user_detail_when_user_does_not_exist(self):
        client = APIClient()
        response = client.get(
            f"/auth/users/{self.user}/",
        )
        self.assertEqual(response.status_code , status.HTTP_404_NOT_FOUND)


class TestMe(APITestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.StaffUser")

    def test_me_when_user_exists(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            "/auth/staffusers/me/",
            
        )
        self.assertEqual(response.status_code , status.HTTP_200_OK)
    

class TestChangePassword(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.StaffUser", password=make_password("old_password"))

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
