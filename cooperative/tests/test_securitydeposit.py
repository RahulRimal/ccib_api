import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateSecurityDeposit(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.security_deposit = baker.make("cooperative.SecurityDeposit")
        cls.loan = baker.make("cooperative.LoanAccount")


    def test_create_security_deposit(self):
        client = APIClient()
        response = client.post(
            "/cooperative/securitydeposits/",
            {
                "loan": self.loan.idx,
                "type": "real state",
                "description": "Test Description",
                "ownership_type": "own",
                "coverage_percentage": 100,
                "nature_of_charge": "first_charge",
                "latest_value": 1000,
                "latest_valuation_date": "2022-01-01"
              
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_create_security_deposit_when_loan_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/securitydeposits/",
            {
                "loan": self.loan.idx,
                "type": "real state",
                "description": "Test Description",
                "ownership_type": "own",
                "coverage_percentage": 100,
                "nature_of_charge": "first_charge",
                "latest_value": 1000,
                "latest_valuation_date": "2022-01-01"
              
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
@pytest.mark.django_db
class TestListSecurityDeposit(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.security_deposit = baker.make("cooperative.SecurityDeposit")
        cls.loan = baker.make("cooperative.LoanAccount")

    def test_list_security_deposit(self):
        client = APIClient()
        response = client.get(
            "/cooperative/securitydeposits/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDetailSecurityDeposit(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.security_deposit = baker.make("cooperative.SecurityDeposit")
        cls.loan = baker.make("cooperative.LoanAccount")

    def test_detail_security_deposit(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/securitydeposits/{self.security_deposit.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestDeleteSecurityDeposit(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.security_deposit = baker.make("cooperative.SecurityDeposit")
        cls.loan = baker.make("cooperative.LoanAccount")

    def test_delete_security_deposit(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/securitydeposits/{self.security_deposit.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


@pytest.mark.django_db
class TestUpdateSecurityDeposit(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.security_deposit = baker.make("cooperative.SecurityDeposit")
        cls.loan = baker.make("cooperative.LoanAccount")

    def test_update_security_deposit(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/securitydeposits/{self.security_deposit.idx}/",
            {
                "type": "real state",
                "description": "Test Description",
                "ownership_type": "own",
                "coverage_percentage": 100,
                "nature_of_charge": "first_charge",
                "latest_value": 10000,
                "latest_valuation_date": "2022-01-01"

            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)        