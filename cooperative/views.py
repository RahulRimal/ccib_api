
from rest_framework.viewsets import ModelViewSet

from finance_cbi.cib.models import Loan, Company
from finance_cbi.cib.serializers import LoanSerializer, CompanySerializer

# Create your views here.


class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
