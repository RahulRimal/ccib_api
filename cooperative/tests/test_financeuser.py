import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateFinanceUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance_user = baker.make("cooperative.FinanceUser")
        cls.user = baker.make("autho.User")


    def test_create_finance_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(
            "/cooperative/financeusers/",
            {
               "first_name": "aa",
               "last_name": "aa",
               "email": "abc@x.com",
               "phone_number": "1234567890",
               "citizenship_number": "1234567890",
               "citizenship_issued_date": "2020-01-01",
               "citizenship_issued_place": "aa",
               "father_name": "aa",
               "mother_name": "aa",
               "grandfather_name": "aa",
               "permanent_address": "aa",
               "temporary_address": "aa",
               "gender": "male",
               "dob": "2020-01-01",
               "date_joined": "2020-01-01",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

@pytest.mark.django_db
class TestListFinanceUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance_user = baker.make("cooperative.FinanceUser")
        cls.user = baker.make("autho.User")


    def test_list_finance_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            "/cooperative/financeusers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestDetailFinanceUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance_user = baker.make("cooperative.FinanceUser")
        cls.user = baker.make("autho.User", is_staff=True)


    def test_detail_finance_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(
            f"/cooperative/financeusers/{self.finance_user.idx}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestUpdateFinanceUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance_user = baker.make("cooperative.FinanceUser")
        cls.user = baker.make("autho.User", is_staff=True)



    def test_update_finance_user(self):
        print(self.finance_user)
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.patch(
            f"/cooperative/financeusers/{self.finance_user.idx}/",
            {
               "first_name": "aa",
               "last_name": "aa",
               "email": "abc@x.com",
               "phone_number": "1234567890",
               "citizenship_number": "1234567890",
               "citizenship_issued_date": "2020-01-01",
               "citizenship_issued_place": "aa",
               "father_name": "aa",
               "mother_name": "aa",
               "grandfather_name": "aa",
               "permanent_address": "aa",
               "temporary_address": "aa",
               "gender": "male",
               "dob": "2020-01-01",
               "date_joined": "2020-01-01",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteFinanceUser(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance_user = baker.make("cooperative.FinanceUser")
        cls.user = baker.make("autho.User", is_staff=True)
        

    def test_delete_finance_user(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
            f"/cooperative/financeusers/{self.finance_user.idx}/",  
            )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)