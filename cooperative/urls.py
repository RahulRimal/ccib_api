from django.urls import path
from. import views

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('loans', views.LoanViewSet, basename='loans')
router.register('companys', views.CompanyViewSet, basename='companys')
router.register('loanapplications', views.LoanApplicationViewSet, basename='loanapplications')
router.register('finance', views.FinanceViewSet, basename='finance')

loan_router = NestedDefaultRouter(router, 'loans', lookup='loan')

loan_router.register('guarantors', views.PersonalGuarantorViewSet, basename='loan-guarantors')


urlpatterns = router.urls + loan_router.urls