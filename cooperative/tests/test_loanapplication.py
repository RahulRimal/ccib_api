import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateLoanApplication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.loanapplication = baker.make("cooperative.LoanApplication")
        cls.finance = baker.make("cooperative.Finance")

    def test_create_loanapplication(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loanapplications/",
            {
                "finance": self.finance.idx,
                "user": self.user.idx,
                "loan_amount": 10000,
                "first_name": "John",
                "middle_name": "A",
                "last_name": "Doe",
                "citizenship_number": "123456789",
                "citizenship_issued_place": "Lagos",
                "citizenship_issued_date": "2022-01-01",
                "father_name": "John",
                "phone_number": "08123456789",
                "status": "pending",

            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    def test_create_loanapplication_without_finance(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loanapplications/",
            {
                "loan_amount": 10000,
                "first_name": "John",
                "middle_name": "A",
                "last_name": "Doe",
                "citizenship_number": "123456789",
                "citizenship_issued_place": "Lagos",
                "citizenship_issued_date": "2022-01-01",
                "father_name": "John",
                "phone_number": "08123456789",
                "status": "pending",

            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

@pytest.mark.django_db
class TestListLoanApplication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loanapplication = baker.make("cooperative.LoanApplication")
        cls.finance = baker.make("cooperative.Finance")

    def test_list_loanapplication(self):
        client = APIClient()
        response = client.get(
            "/cooperative/loanapplications/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDetailLoanApplication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loanapplication = baker.make("cooperative.LoanApplication")
        cls.finance = baker.make("cooperative.Finance")

    def test_detail_loanapplication(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/loanapplications/{self.loanapplication.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestUpdateLoanApplication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loanapplication = baker.make("cooperative.LoanApplication")
        cls.finance = baker.make("cooperative.Finance")

    def test_update_loanapplication(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/loanapplications/{self.loanapplication.idx}/",
            {
                "status": "approved",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteLoanApplication(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loanapplication = baker.make("cooperative.LoanApplication")
        cls.finance = baker.make("cooperative.Finance")

    def test_delete_loanapplication(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/loanapplications/{self.loanapplication.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)