from django.contrib import admin

from cooperative.models import Blacklist, BlacklistReport, Company, Finance, FinanceStaff, FinanceUser, Inquiry, Installment, LoanAccount, LoanApplication, PersonalGuarantor, SecurityDeposit


# class PersonalGuarantorInLineAdmin(admin.TabularInline):
#     model = PersonalGuarantor
#     extra = 1
#     max_num = 3
#     min_num = 2
#     list_display = ["idx", "user"]


@admin.register(LoanAccount)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "name",
        "loan_nature",
        "loan_amount",
        "maturity_date",
        "installment_due_type",
        "installment_amount",
        "total_outstanding",
        "overdue_amount",
    ]
    # inlines = [PersonalGuarantorInLineAdmin]

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

@admin.register(FinanceStaff)
class FinanceStaffAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "finance",
    ]

@admin.register(FinanceUser)
class FinanceStaffAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "first_name",
        "last_name"
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

