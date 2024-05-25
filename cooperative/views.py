from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from cooperative.models import (
    Company,
    Finance,
    Installment,
    Loan,
    LoanApplication,
    PersonalGuarantor,
    SecurityDeposit,
)

from cooperative.serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    CreateInstallmentSerializer,
    CreateLoanApplicationSerializer,
    CreateLoanSerializer,
    CreatePersonalGuarantorSerializer,
    CreateSecurityDepositSerializer,
    FinanceSerializer,
    InstallmentSerializer,
    LoanApplicationSerializer,
    LoanSerializer,
    PersonalGuarantorSerializer,
    SecurityDepositSerializer,
    UpdateCompanySerializer,
    UpdateLoanApplicationSerializer,
    UpdateLoanSerializer,
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


class LoanViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Loan.objects.all()
    filterset_fields = ["status","user", "account_number"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanSerializer
        if self.request.method == "PATCH":
            return UpdateLoanSerializer
        return LoanSerializer


class LoanApplicationViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = LoanApplication.objects.all()
    filterset_fields = ["status","user", "finance"]

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
    filterset_fields = ["loan"]
 
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