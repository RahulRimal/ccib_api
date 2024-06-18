import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateFinanceStaff(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")
        cls.finance = baker.make("cooperative.Finance")

    def test_create_finance_staff(self):
        client = APIClient()
        response = client.post(
            "/cooperative/financestaffs/",
            {
                "user": self.user.idx,
                "finance": self.finance.idx
            },
            
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_finance_staff_when_finance_staff_exists(self):
        client = APIClient()
        response = client.post(
            "/cooperative/financestaffs/",
            {
                "finance": self.finance.idx
            },
            
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_finance_staff_when_finance_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/financestaffs/",
            {
                "user": self.user.idx
            },
            
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_finance_staff_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/financestaffs/",
            {
                "finance": self.finance.idx
            },
            
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestListFinanceStaff(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")
        cls.finance = baker.make("cooperative.Finance")

    def test_list_finance_staff(self):
        client = APIClient()
        response = client.get(
            "/cooperative/financestaffs/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

