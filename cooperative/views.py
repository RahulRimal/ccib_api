from collections import defaultdict
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import F, Max, Min, Prefetch, Q, Count

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


from autho.models import User
from common.api_response import api_response_error, api_response_success
from common.mixins import BaseApiMixin
from common.helpers import get_local_date
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

    @action(detail=False, methods=["GET"])
    def loan_status_overview(self, request):
        status_counts = LoanAccount.objects.values("status").annotate(
            count=Count("status")
        )

        results = {status: 0 for status, _ in LoanAccount.STATUS_CHOICES}

        for status_count in status_counts:
            results[status_count["status"]] = status_count["count"]

        return api_response_success(results)


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

    @action(detail=False, methods=["GET"])
    def quick_summary(self, request):
        finance = Finance.objects.filter(
            idx=request.query_params.get("finance_idx")
        ).first()
        total_users = User.objects.count()

        total_active_loans = LoanAccount.objects.filter(
            status="active", finance=finance
        ).count()

        data = {"total_users": total_users, "total_active_loans": total_active_loans}

        return api_response_success(data)

    @action(detail=False, methods=["GET"])
    def income_overview(self, request):
        one_year_ago = datetime.now().date() - timedelta(days=365)
        installments = Installment.objects.filter(due_date__lte=one_year_ago)

        monthly_data = defaultdict(lambda: {"total_due": 0, "total_paid": 0})

        for installment in installments:
            month = installment.due_date.strftime("%Y-%m")
            monthly_data[month]["total_due"] += installment.total_due
            monthly_data[month]["total_paid"] += installment.total_paid

        sorted_monthly_data = dict(sorted(monthly_data.items()))

        response_data = []
        for month, data in sorted_monthly_data.items():
            response_data.append(
                {
                    "date": month + "-01",
                    "total_due": data["total_due"],
                    "total_paid": data["total_paid"],
                }
            )

        return api_response_success(response_data)

    @action(detail=False, methods=["GET"])
    def overdue_loans(self, request):
        finance_idx = request.query_params.get("finance")

        # Get the current date
        current_date = get_local_date()

        # Prefetch related objects and annotate the latest installment's due date for each loan account
        loan_accounts = (
            LoanAccount.objects.filter(finance__idx=finance_idx)
            .select_related("user")
            .prefetch_related(
                Prefetch(
                    "installments",
                    queryset=Installment.objects.filter(
                        due_date__lte=current_date, total_outstanding__gt=0
                    ),
                )
            )
            .annotate(
                latest_due_date=Max(
                    "installments__due_date",
                    filter=Q(
                        installments__due_date__lte=current_date,
                        installments__total_outstanding__gt=0,
                    ),
                )
            )
            .filter(latest_due_date__isnull=False)
        )

        response_data = []
        for loan_account in loan_accounts:
            latest_installment = loan_account.installments.filter(
                due_date=loan_account.latest_due_date
            ).latest("due_date")
            response_data.append(
                {
                    "due_date": latest_installment.due_date,
                    "status": loan_account.status,
                    "user": loan_account.user.first_name,
                    "total_due_amount": latest_installment.total_due,
                }
            )

        return api_response_success(response_data)


class InstallmentViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Installment.objects.all()
    filterset_fields = ["loan", "due_date", "total_outstanding"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateInstallmentSerializer
        return InstallmentSerializer

    @action(detail=False, methods=["GET"])
    def credit_profile_summary(self, request):
        user_idx = request.query_params.get("user")
        if not user_idx:
            return api_response_error("User ID is required", status=400)

        user = User.objects.filter(idx=user_idx).first()
        if not user:
            return api_response_error("User not found", status=404)

        # Assuming Installment has a foreign key to Loan and Loan has a foreign key to User
        installments = Installment.objects.filter(loan__user=user)
        credit_profile = []

        for installment in installments:
            profile_entry = {
                "date": installment.created_at,
                "installment_paid": installment.total_paid,
                "amount_overdue": installment.total_due - installment.total_paid,
            }
            credit_profile.append(profile_entry)

        return api_response_success(credit_profile)

    @action(detail=False, methods=["GET"])
    def user_credit_profile_overview(self, request):
        user_idx = request.query_params.get("user")
        if not user_idx:
            return api_response_error("User ID is required", status=400)

        user = User.objects.filter(idx=user_idx).first()
        if not user:
            return api_response_error("User not found", status=404)

        installment_stats = (
            Installment.objects.filter(loan__user=user)
            .annotate(due_days=F("paid_date") - F("due_date"))
            .aggregate(max_days=Max("due_days"), min_days=Min("due_days"))
        )

        total_due_installments = Installment.objects.filter(
            loan__user=user, due_date__lt=timezone.now(), total_paid=0
        ).count()

        loan_utilization_stats = LoanAccount.objects.filter(user=user).aggregate(
            max_utilization=Max("utilization_percent"),
            min_utilization=Min("utilization_percent"),
        )

        overview_data = {
            "max_due_days": installment_stats.get("max_days").days or 0,
            "min_due_days": installment_stats.get("min_days").days or 0,
            "total_due_installments": total_due_installments,
            "max_utilization_percent": loan_utilization_stats.get("max_utilization"),
            "min_utilization_percent": loan_utilization_stats.get("min_utilization"),
        }

        return api_response_success(overview_data)

  
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
    filterset_fields = ["user__idx"]
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
    filterset_fields = ["user"]
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

        return api_response_success(return_data)
