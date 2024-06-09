import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateInstallment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
    

    def test_create_installment(self):
        client = APIClient()
        response = client.post(
            "/cooperative/installments/",
            {
                "loan": self.loan.idx,
                "due_date": "2022-01-01",
                "total_due": 1000,
                "paid_date": "2022-01-01",
                "total_paid": 1000,
                "total_outstanding": 1000
            },
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
    

@pytest.mark.django_db
class TestUpdateInstallment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_update_installment(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/installments/{self.installment.idx}/",
            {
                "loan": self.loan.idx,
                "due_date": "2022-01-01",
                "total_due": 1000,
                "paid_date": "2022-01-01",
                "total_paid": 1000,
                "total_outstanding": 1000
            },
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

@pytest.mark.django_db
class TestDeleteInstallment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_delete_installment(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/installments/{self.installment.idx}/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )

@pytest.mark.django_db
class TestListInstallment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_list_installment(self):
        client = APIClient()
        response = client.get(
            "/cooperative/installments/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

@pytest.mark.django_db
class TestDetailInstallment(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_detail_installment(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/installments/{self.installment.idx}/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


