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


@pytest.mark.django_db
class CreaditProfileSummary(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.loan = baker.make("cooperative.LoanAccount")
        cls.user = baker.make("autho.User")
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_credit_profile_summary(self):
        client = APIClient()
        response = client.get(
            "/cooperative/installments/credit_profile_summary/",
            {
                "user": self.user.idx,
                "date":self.installment.created_at,
                "installment_paid": self.installment.total_paid,
                "amount_overdue": self.installment.total_due - self.installment.total_paid

            }
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )




@pytest.mark.django_db
class UserCreditProfileOverview(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("autho.User")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user)
        cls.installment = baker.make("cooperative.Installment", loan=cls.loan)

    def test_user_credit_profile_overview(self):
        client = APIClient()
        response = client.get(
            "/cooperative/installments/user_credit_profile_overview/",
            {"user": self.user.idx,
             "max_due_days": 2,
             "min_due_days": 1,
             "total_due_installments": 3,
             "max_utilization_percent": 100,
             "min_utilization_percent": 0,
             "total_utilization_percent": 50
             
             }
        )

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )






