import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker

@pytest.mark.django_db
class TestCreateInguiry(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.inquirer = baker.make("cooperative.FinanceStaff")
        cls.finance = baker.make("cooperative.Finance")

    def test_create_inguiry(self):
        client = APIClient()
        response = client.post(
            "/cooperative/inquiries/",
            {
                "inquirer": self.inquirer.idx,
                "user": self.user.idx,
                "finance": self.finance.idx,
                "reason": "Test Reason",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_inguiry_when_inquirer_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/inquiries/",
            {
                "inquirer": 1,
                "user": self.user.idx,
                "finance": self.finance.idx,
                "reason": "Test Reason",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_create_inguiry_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/inquiries/",
            {
                "inquirer": self.inquirer.idx,
                "finance": self.finance.idx,
                "reason": "Test Reason",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_create_inguiry_when_finance_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/inquiries/",
            {
                "inquirer": self.inquirer.idx,
                "user": self.user.idx,
                "reason": "Test Reason",

            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestListInguiry(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_list_inguiry(self):
        client = APIClient()
        response = client.get(
            "/cooperative/inquiries/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDetailInguiry(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.inguiry = baker.make("cooperative.Inquiry")

    def test_detail_inguiry(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/inquiries/{self.inguiry.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestUpdateInguiry(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.inguiry = baker.make("cooperative.Inquiry")

    def test_update_inguiry(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/inquiries/{self.inguiry.idx}/",
            {
                "reason": "Test Reason",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


