from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from cooperative.models import Company, Loan, LoanApplication, PersonalGuarantor
from cooperative.serializers import (
    CompanySerializer,
    CreateCompanySerializer,
    CreateLoanApplicationSerializer,
    CreateLoanSerializer,
    CreatePersonalGuarantorSerializer,
    LoanApplicationSerializer,
    LoanSerializer,
    PersonalGuarantorSerializer,
    UpdateCompanySerializer,
    UpdateLoanApplicationSerializer,
    UpdateLoanSerializer,
    UpdatePersonalGuarantorSerializer,
)


# Create your views here.
class PersonalGuarantorViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = PersonalGuarantor.objects.all()
    # serializer_class = PersonalGuarantorSerializer

    def get_queryset(self):
        return PersonalGuarantor.objects.filter(loan__idx=self.kwargs["loan_idx"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePersonalGuarantorSerializer
        if self.request.method == "PATCH":
            return UpdatePersonalGuarantorSerializer
        return PersonalGuarantorSerializer
    
    def get_serializer_context(self):
        return {"loan_idx": self.kwargs["loan_idx"]}
    


class LoanViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = Loan.objects.all()
    # serializer_class = LoanSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanSerializer
        if self.request.method == "PATCH":
            return UpdateLoanSerializer
        return LoanSerializer


class LoanApplicationViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    queryset = LoanApplication.objects.all()
    # serializer_class = LoanApplicationSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateLoanApplicationSerializer
        if self.request.method == "PATCH":
            return UpdateLoanApplicationSerializer
        return LoanApplicationSerializer


class CompanyViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Company.objects.all()
    # serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCompanySerializer
        if self.request.method == "PATCH":
            return UpdateCompanySerializer
        return CompanySerializer
