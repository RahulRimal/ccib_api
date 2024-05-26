from django.utils import timezone
from django.db.models import F, Max, Min

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from rest_framework.decorators import action


from autho.models import User
from common.api_response import api_response_success
from common.mixins import BaseApiMixin
from cooperative.models import (
    Blacklist,
    BlacklistReport,
    Company,
    Finance,
    Inquiry,
    Installment,
    LoanAccount,
    LoanApplication,
    PersonalGuarantor,
    SecurityDeposit,
)

from cooperative.serializers import (
    BlacklistReportSerializer,
    BlacklistSerializer,
    CompanySerializer,
    CreateBlacklistReportSerializer,
    CreateBlacklistSerializer,
    CreateCompanySerializer,
    CreateInquirySerializer,
    CreateInstallmentSerializer,
    CreateLoanAccountSerializer,
    CreateLoanApplicationSerializer,
    CreatePersonalGuarantorSerializer,
    CreateSecurityDepositSerializer,
    FinanceSerializer,
    InquirySerializer,
    InstallmentSerializer,
    LoanApplicationSerializer,
    LoanAccountSerializer,
    PersonalGuarantorSerializer,
    SecurityDepositSerializer,
    UpdateCompanySerializer,
    UpdateLoanAccountSerializer,
    UpdateLoanApplicationSerializer,
)


class PersonalGuarantorViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = PersonalGuarantor.objects.all()

    def get_queryset(self):
        return PersonalGuarantor.objects.filter(loan__idx=self.kwargs["loan_idx"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePersonalGuarantorSerializer
        return PersonalGuarantorSerializer

    def get_serializer_context(self):
        return {"loan_idx": self.kwargs["loan_idx"]}


class LoanAccountViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = LoanAccount.objects.all()
    filterset_fields = ["status", "user", "account_number", "loan_type"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanAccountSerializer
        if self.request.method == "PATCH":
            return UpdateLoanAccountSerializer
        return LoanAccountSerializer


class LoanApplicationViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = LoanApplication.objects.all()
    filterset_fields = ["status", "user", "finance"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanApplicationSerializer
        if self.request.method == "PATCH":
            return UpdateLoanApplicationSerializer
        return LoanApplicationSerializer


class CompanyViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Company.objects.all()
    filterset_fields = ["name", "pan_num", "vat_num"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCompanySerializer
        if self.request.method == "PATCH":
            return UpdateCompanySerializer
        return CompanySerializer


class FinanceViewSet(BaseApiMixin, ModelViewSet):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer
    filterset_fields = ["name"]


class InstallmentViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Installment.objects.all()
    filterset_fields = ["loan", "due_date", "total_outstanding"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateInstallmentSerializer
        return InstallmentSerializer


class SecurityDepositViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = SecurityDeposit.objects.all()
    filterset_fields = ["loan", "type", "ownership_type"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateSecurityDepositSerializer
        return SecurityDepositSerializer


class BlacklistViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Blacklist.objects.all()
    # serializer_class = BlacklistSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBlacklistSerializer
        return BlacklistSerializer


class BlacklistReportViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = BlacklistReport.objects.all()
    # serializer_class = BlacklistReportSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBlacklistReportSerializer
        return BlacklistReportSerializer


class InquiryViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Inquiry.objects.all()
    # serializer_class = BlacklistSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateInquirySerializer
        return InquirySerializer


class ReportView(BaseApiMixin, APIView):

    # @action(detail=False, methods = ['GET'])
    # def summary(self, request):
    def get(self, request):
        user = User.objects.last()

        blacklist = Blacklist.objects.filter(user=user).first()
        user_loan_accounts = LoanAccount.objects.all()

        loan_accounts_list = []
        for loan_account in user_loan_accounts:
            finance_name = loan_account.finance.name
            for loan_account_item in loan_accounts_list:
                if loan_account_item["finance_name"] == finance_name:
                    loan_account_item["total_amount"] += loan_account.total_loan
                    loan_account_item["outstanding"] += loan_account.loan_outstanding
                    loan_account_item["overdue_amount"] += loan_account.overdue_amount
                    loan_account_item["total_account"] += 1
                    break
            else:
                loan_accounts_list.append(
                    {
                        "finance_name": finance_name,
                        "total_amount": loan_account.total_loan,
                        "outstanding": loan_account.loan_outstanding,
                        "overdue_amount": loan_account.overdue_amount,
                        "total_account": 1
                    }
                )

        installment = (
            Installment.objects.all()
            .annotate(due_days=F("paid_date") - F("due_date"))
            .aggregate(max_days=Max("due_days"), min_days=Min("due_days"))
        )

        total_due_installment = Installment.objects.filter(
            due_date__lt=timezone.now(), total_paid=0
        ).count()

        loan_utilization = LoanAccount.objects.all().aggregate(
            Max("utilization_percent"), Min("utilization_percent")
        )

        total_installments = Installment.objects.all()

        # user_account_list =[]

        # for user_account in user_loan_accounts:
        #     user_account_list.append(
        #         {
        #             "number_of_account": user_account.account_number,
        #             "type_of_loan": user_account.loan_type,
        #             "finance_name": user_account.finance.name,
        #             "outstanding_balance": user_account.loan_outstanding,
        #             "utilization_percent_creadit": user_account.utilization_percent,
        #             "amount_overdue": user_account.total_loan - user_account.total_paid


                    

        #         }
        #     )

        return_data = {}
        return_data["quick_report"] = {
            "evalution": 180,
            "probability": 0.5,
            "rank": "prime a",
            "evalution_date": "2020-01-01",
            "evalution_date_range": ["2020-01-01", "2020-01-31"],
            "summary": "lorem ipsum dolor sit amet",
            "categories": {
                "categories": [
                    {
                        "name": "risk",
                        "lower_limit": 0,
                        "upper_limit": 25,
                    },
                    {
                        "name": "prime",
                        "lower_limit": 26,
                        "upper_limit": 50,
                    },
                    {
                        "name": "ultimate",
                        "lower_limit": 51,
                        "upper_limit": 75,
                    },
                    {
                        "name": "elite",
                        "lower_limit": 76,
                        "upper_limit": 100,
                    },
                ],
            },
        }

        return_data["score_history"] = [
            {"date": "2020-01-01", "score": 100},
            {"date": "2020-01-02", "score": 130},
            {"date": "2020-01-03", "score": 390},
            {"date": "2020-01-04", "score": 600},
            {"date": "2020-01-04", "score": 983},
        ]

        return_data["report_details"] = {
            "name": user.first_name + " " + user.last_name,
            "gender": user.gender,
            "father_name": user.father_name,
            "mother_name": user.mother_name,
            "last_name": user.last_name,
            "permanent_address": user.permanent_address,
            "temporary_address": user.temporary_address,
            "cir_number": user.idx,
            "dob": user.dob,
            "email": user.email,
            "phone_number": user.phone_number,
            "citizenship_number": user.citizenship_number,
            "citizenship_issued_place": user.citizenship_issued_place,
            "citizenship_issued_date": user.citizenship_issued_date,
        }

        return_data["search_details"] = {
            "name": user.first_name + " " + user.last_name,
            "gender": user.gender,
            "father_name": user.father_name,
            "mother_name": user.mother_name,
            "last_name": user.last_name,
            "permanent_address": user.permanent_address,
            "temporary_address": user.temporary_address,
            "dob": user.dob,
            "email": user.email,
            "phone_number": user.phone_number,
            "citizenship_number": user.citizenship_number,
            "citizenship_issued_place": user.citizenship_issued_place,
            "citizenship_issued_date": user.citizenship_issued_date,
            "nationality": "nepal",
            "search_confidience_score": 100,
        }

        return_data["consumer_details"] = {
            "name": user.first_name + " " + user.last_name,
            "gender": user.gender,
            "father_name": user.father_name,
            "mother_name": user.mother_name,
            "grandfather_name": user.grandfather_name,
            "last_name": user.last_name,
            "permanent_address": user.permanent_address,
            "temporary_address": user.temporary_address,
            "dob": user.dob,
            "phone_number": user.phone_number,
            "citizenship_number": user.citizenship_number,
            "citizenship_issued_place": user.citizenship_issued_place,
            "citizenship_issued_date": user.citizenship_issued_date,
            "nationality": "nepal",
            "marital_status": "single",
        }
        if blacklist:
            return_data["blacklist_history"] = {
                "blacklist_id": blacklist.id,
                "status": blacklist.status,
                "finance": blacklist.finance.name,
                "reason": blacklist.reason,
                "category": blacklist.category,
                "release_date": blacklist.release_date,
                "remarks": blacklist.remarks,
                "report_date": blacklist.report_date,
            }

        return_data["user_accounts"] = loan_accounts_list

        return_data["credit_prpfile_overview"] = {
            "max_due_days": installment.get("max_days").days or 0,
            "min_due_day": installment.get("min_days").days or 0,
            "toal_due_installment": total_due_installment,
            "max_utilization_percent": loan_utilization.get("utilization_percent__max"),
            "min_utilization_percent": loan_utilization.get("utilization_percent__min"),
        }

        return_data["credit_prpfile_summary"] = [
            {
                "date": installment.created_at,
                "installment_paid": installment.total_paid,
                "amount_overdue": installment.total_due - installment.total_paid,
            }
            for installment in total_installments
        ]

        # return_data["user_accounts_type"] = user_account_list

        return api_response_success(return_data)
