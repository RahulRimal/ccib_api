from django.contrib import admin

from cooperative.models import Blacklist, BlacklistReport, Company, Finance, Inquiry, Installment, LoanAccount, LoanApplication, PersonalGuarantor, SecurityDeposit


# Register your models here.


class PersonalGuarantorInLineAdmin(admin.TabularInline):
    model = PersonalGuarantor
    extra = 1
    max_num = 3
    min_num = 2
    list_display = ["idx", "user"]


@admin.register(LoanAccount)
class LoanAccountAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "account_number",
        "total_loan",
        "total_paid",
        "loan_outstanding",
        "loan_limit",
        "interest_rate",
        "overdue_amount",
        "status",
        "loan_type",
        "is_closed",
        "utilization_percent",
    ]
    inlines = [PersonalGuarantorInLineAdmin]

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "loan_amount",
        "finance",
        "status",
    ]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "name",
        "pan_num",
        "vat_num",
        "permanent_add",
        "pan_registration_date",
        "pan_registration_place",
        "profiter",
        "lone_taker_type",
    ]

@admin.register(Finance)
class FinanceAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "name",
        "description",
        "location",
    ]


@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "loan",
        "paid_date",
        "due_date",
        "total_due",
        "total_paid",
        "total_outstanding",
    ]


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "finance",
        "status",
        "release_date",
        "report_date",
        "category",
        "reason",
        "remarks",
    ]


@admin.register(BlacklistReport)
class BlacklistReportAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "finance",
        "status",
    ]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "finance",
        "reason",
        "inquirer",
    ]


@admin.register(SecurityDeposit)
class SecurityDepositAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "loan",
        "type",
        "description",
        "ownership_type",
        "coverage_percentage",
        "nature_of_charge",
        "latest_value",
        "latest_valuation_date",
    ]

