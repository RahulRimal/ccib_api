import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker

@pytest.mark.django_db
class TestCreateLoanAccount(APITestCase):   
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")

    def test_create_loan_account(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "user": self.user.idx,
                "finance": self.finance.idx,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )


    def test_create_loan_account_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "user": self.user,
                "finance": self.finance,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
    
    def test_create_loan_account_when_finance_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "finance": self.finance,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
    

    def test_create_loan_account_when_finance_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "user": self.user,
                "finance": self.finance,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )

    def test_create_loan_account_when_user_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "user": self.user.idx,
                "finance": self.finance,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
    
    def test_create_loan_account_when_user_and_finance_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/loans/",
            {
                "account_number": "1234567890",
                "user": self.user.idx,
                "finance": self.finance.idx,
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "is_closed": False,
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )


@pytest.mark.django_db
class TestUpdateLoanAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_update_loan_account(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/loans/{self.loan.idx}/",
            {
                "account_number": "1234567890",
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
    
    def test_update_loan_account_when_loan_does_not_exist(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/loans/{self.loan}/",
            {
                "account_number": "1234567890",
                "name": "test",
                "loan_amount": 1000,
                "interest_rate": 10,
                "loan_limit": 1000,
                "maturity_date": "2022-01-01",
                "installment_amount": 100,
                "installment_due_type": "daily",
                "total_paid": 0,
                "loan_nature": "term",
                "overdue_amount": 500,
                "utilization_percent": 0,
                "status": "good"
                
                },
            
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )


@pytest.mark.django_dbS
class  TestDeleteLoanAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_delete_loan_account(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/loans/{self.loan.idx}/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
    
    def test_delete_loan_account_when_loan_does_not_exist(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/loans/{self.loan}/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_404_NOT_FOUND
        )
    
@pytest.mark.django_db
class TestListLoanAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_list_loan_account(self):
        client = APIClient()
        response = client.get(
            "/cooperative/loans/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

@pytest.mark.django_db
class TestDetailLoanAccount(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_detail_loan_account(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/loans/{self.loan.idx}/",
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )



class TestOverDueLoans(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.installment = baker.make("cooperative.Installment")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_overdue_loans(self):
        client = APIClient()
        response = client.get(
            "/cooperative/loans/overdue_loans/",
            {
                "due_date": "2022-01-01",
                "status": "good",
                "user": self.user.first_name,
                "total_due_amount": 0

            },
        )


        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


@pytest.mark.django_db
class TestListOverdueLoans(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_list_overdue_loans(self):
        client = APIClient()
        response = client.get(
            "/cooperative/loans/overdue_loans/",
            {
                "due_date": "2022-01-01",
                "status": "good",
                "user": self.user.first_name,
                "total_due_amount": 0

            },
        )


        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
    
@pytest.mark.django_db
class TestLoanStatusOverview(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")
        cls.loan = baker.make("cooperative.LoanAccount", user=cls.user, finance=cls.finance)

    def test_loan_status_overview(self):
        client = APIClient()
        response = client.get(
            "/cooperative/loans/loan_status_overview/",

        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )


