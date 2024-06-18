import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker

@pytest.mark.django_db
class TestCreateCompany(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")

    def test_create_company(self):
        client = APIClient()
        response = client.post(
            "/cooperative/companys/",
            {
                "name": "Test Company",
                "pan_num": "123456789",
                "vat_num": "123456789",
                "permanent_add": "Test Address",
                "pan_registration_date": "2022-01-01",
                "pan_registration_place": "Test Place",
                "profiter": self.user.idx,
                "lone_taker_type": "company",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
@pytest.mark.django_db
class TestUpdateCompany(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.company = baker.make("cooperative.Company")

    def test_update_company(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/companys/{self.company.idx}/",
            {
                "name": "Test Company",
                "pan_num": "123456789",
                "vat_num": "123456789",
                "permanent_add": "Test Address",
                "pan_registration_date": "2022-01-01",
                "pan_registration_place": "Test Place",
                "lone_taker_type": "company",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteCompany(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.company = baker.make("cooperative.Company")

    def test_delete_company(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/companys/{self.company.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

@pytest.mark.django_db
class TestListCompany(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.company = baker.make("cooperative.Company")

    def test_list_company(self):
        client = APIClient()
        response = client.get(
            "/cooperative/companys/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestDetailCompany(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.company = baker.make("cooperative.Company")

    def test_detail_company(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/companys/{self.company.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    


