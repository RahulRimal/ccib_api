from django.urls import path
from. import views 
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('loans', views.LoanAccountViewSet, basename='loans')
router.register('companys', views.CompanyViewSet, basename='companys')
router.register('loanapplications', views.LoanApplicationViewSet, basename='loanapplications')
router.register('finance', views.FinanceViewSet, basename='finance')
router.register('installments', views.InstallmentViewSet, basename='installments')
router.register('securitydeposits', views.SecurityDepositViewSet, basename='securitydeposits')
router.register('inquiries', views.InquiryViewSet, basename='inquiries')
router.register('blacklists', views.BlacklistViewSet, basename='blacklists')
router.register('blacklistreports', views.BlacklistReportViewSet, basename='blacklistreports')
router.register('financestaffs', views.FinanceStaffViewSet, basename='financestaffs')
# router.register('reports', views.ReportViewSet, basename='reports')

loan_router = NestedDefaultRouter(router, 'loans', lookup='loan')

loan_router.register('guarantors', views.PersonalGuarantorViewSet, basename='loan-guarantors')

urlpatterns = [
    path("report", views.ReportView.as_view(), name="report"),
]
urlpatterns += router.urls + loan_router.urls