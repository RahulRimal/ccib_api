import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateFinance(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")

    def test_create_finance(self):
        client = APIClient()
        response = client.post(
            "/cooperative/finance/",
            {
                "name": "aa",
                "description": "Test Description",
                "location": {"name": "aas"},
                "email": "abc@x.com",
                "phone_number": "1234567890",
                "website_url": "https://aa.com",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


@pytest.mark.django_db
class TestListFinance(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")

    def test_list_finance(self):
        client = APIClient()
        response = client.get(
            "/cooperative/finance/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestDetailFinance(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")

    def test_detail_finance(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/finance/{self.finance.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestUpdateFinance(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")

    def test_update_finance(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/finance/{self.finance.idx}/",
            {
                "name": "Test Finance",
                "description": "Test Description",
                "location": {"name": "Test Location"},
                "email": "abc@x.com",
                "phone_number": "1234567890",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteFinance(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")

    def test_delete_finance(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/finance/{self.finance.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)