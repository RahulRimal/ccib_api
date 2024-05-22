from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from cooperative.models import (
    Company,
    Finance,
    Installment,
    Loan,
    LoanApplication,
    PersonalGuarantor,
    Security,
)

from cooperative.serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    CreateInstallmentSerializer,
    CreateLoanApplicationSerializer,
    CreateLoanSerializer,
    CreatePersonalGuarantorSerializer,
    CreateSecuritySerializer,
    FinanceSerializer,
    InstallmentSerializer,
    LoanApplicationSerializer,
    LoanSerializer,
    PersonalGuarantorSerializer,
    SecuritySerializer,
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

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanSerializer
        if self.request.method == "PATCH":
            return UpdateLoanSerializer
        return LoanSerializer


class LoanApplicationViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = LoanApplication.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanApplicationSerializer
        if self.request.method == "PATCH":
            return UpdateLoanApplicationSerializer
        return LoanApplicationSerializer


class CompanyViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Company.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCompanySerializer
        if self.request.method == "PATCH":
            return UpdateCompanySerializer
        return CompanySerializer


class FinanceViewSet(BaseApiMixin, ModelViewSet):
    queryset = Finance.objects.all()
    serializer_class = FinanceSerializer


class InstallmentViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Installment.objects.all()
 
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateInstallmentSerializer
        return InstallmentSerializer

class SecurityViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Security.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateSecuritySerializer
        return SecuritySerializer