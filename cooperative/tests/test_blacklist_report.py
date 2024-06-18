import pytest

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from model_bakery import baker


@pytest.mark.django_db
class TestCreateBlacklistReport(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.finance = baker.make("cooperative.Finance")
        cls.user = baker.make("cooperative.FinanceUser")

    def test_create_blacklist_report(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklistreports/",
            {
                "finance": self.finance.idx,
                "user": self.user.idx,
                "status": "progress",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_blacklist_report_when_user_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklistreports/",
            {
                "finance": self.finance.idx,
                "status": "progress",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_blacklist_report_when_finance_does_not_exist(self):
        client = APIClient()
        response = client.post(
            "/cooperative/blacklistreports/",
            {
                "status": "progress",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
class TestListBlacklistReport(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.BlacklistReport")

    def test_list_blacklist_report(self):
        client = APIClient()
        response = client.get(
            "/cooperative/blacklistreports/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDetailBlacklistReport(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.BlacklistReport")

    def test_detail_blacklist_report(self):
        client = APIClient()
        response = client.get(
            f"/cooperative/blacklistreports/{self.blacklist.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestUpdateBlacklistReport(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.BlacklistReport")

    def test_update_blacklist_report(self):
        client = APIClient()
        response = client.patch(
            f"/cooperative/blacklistreports/{self.blacklist.idx}/",
            {
                "status": "approved",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestDeleteBlacklistReport(APITestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.blacklist = baker.make("cooperative.BlacklistReport")
        cls.user = baker.make("autho.User")

    def test_delete_blacklist_report(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(
            f"/cooperative/blacklistreports/{self.blacklist.idx}/",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
