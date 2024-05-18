from django.contrib import admin

from cooperative.models import Company, Loan, LoanApplication, PersonalGuarantor


# Register your models here.


class PersonalGuarantorInLineAdmin(admin.TabularInline):
    model = PersonalGuarantor
    extra = 1
    max_num = 3
    min_num = 2
    list_display = ["idx", "user"]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "name",
        "nature",
        "amount",
        "maturity_date",
        "installment_due_type",
        "emi_amount",
        "currently_outstanding",
        "total_due",
    ]
    inlines = [PersonalGuarantorInLineAdmin]


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "loan_amount",
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
