import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateBlacklist(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.Blacklist")
        cls.user = baker.make("cooperative.FinanceUser")
        cls.finance = baker.make("cooperative.Finance")

    def test_create_blacklist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklists/",
            {

                "user": self.user.idx,
                "finance": self.finance.idx,
                "category": "borrower",
                "reason": "Test Reason",
                "remarks": "Test Remarks",
                "status": "blacklisted",
                "release_date": "2022-01-01",
                "report_date": "2022-01-01",

            },    
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_blacklist_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklists/",
            {
                "finance": self.finance.idx,
                "category": "borrower",
                "reason": "Test Reason",
                "remarks": "Test Remarks",
                "status": "blacklisted",
                "release_date": "2022-01-01",
                "report_date": "2022-01-01",

            },    
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blacklist_when_finance_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklists/",
            {
                "user": self.user.idx,
                "category": "borrower",
                "reason": "Test Reason",
                "remarks": "Test Remarks",
                "status": "blacklisted",
                "release_date": "2022-01-01",
                "report_date": "2022-01-01",

            },    
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
@pytest.mark.django_db
class TestUpdateBlacklist(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.Blacklist")
        cls.finance = baker.make("cooperative.Finance")

    def test_update_blacklist(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/blacklists/{self.blacklist.idx}/",
            {
                "category": "borrower",
                "reason": "Test Reason",
                "remarks": "Test Remarks",
                "status": "blacklisted",
                "release_date": "2022-01-01",
                "report_date": "2022-01-01",    

            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestListBlacklist(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.Blacklist")
        cls.finance = baker.make("cooperative.Finance")

    def test_list_blacklist(self):
        client = APIClient()
        response = client.get(
            "/cooperative/blacklists/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.mark.django_db
class TestDetailBlacklist(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.Blacklist")
        cls.finance = baker.make("cooperative.Finance")

    def test_detail_blacklist(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/blacklists/{self.blacklist.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteBlacklist(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.Blacklist")
        cls.finance = baker.make("cooperative.Finance")

    def test_delete_blacklist(self):
        client = APIClient()
        response = client.delete(
            f"/cooperative/blacklists/{self.blacklist.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

