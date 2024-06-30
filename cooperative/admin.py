from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from cooperative.models import (
    Blacklist,
    BlacklistReport,
    Company,
    Finance,
    FinanceStaff,
    FinanceUser,
    Inquiry,
    Installment,
    LoanAccount,
    LoanApplication,
    PersonalGuarantor,
    SecurityDeposit,
)
from cooperative.utils import import_finance_from_excel, import_finance_user_from_excel, import_installments_from_excel, import_loan_accounts_from_excel, import_loan_applications_from_excel


# class PersonalGuarantorInLineAdmin(admin.TabularInline):
#     model = PersonalGuarantor
#     extra = 1
#     max_num = 3
#     min_num = 2
#     list_display = ["idx", "user"]


class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        # Pop fields from kwargs to dynamically generate form fields
        fields = kwargs.pop("fields", None)
        super(ExcelImportForm, self).__init__(*args, **kwargs)

        if fields:
            for field in fields:
                self.fields[field["name"]] = field["type"](**field.get("params", {}))


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

    change_list_template = "admin/cooperative/excel_import_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-loans/", self.import_loans),
        ]
        return my_urls + urls

    def import_loans(self, request):
        if request.method == "POST":
            file = request.FILES["excel_file"]
            finance = request.POST.get("finance")
            if finance:
                finance = Finance.objects.get(id=finance)
            imported = import_loan_accounts_from_excel(file)
            if not imported:
                self.message_user(request, "Error importing loans.")
                return redirect("..")
            self.message_user(request, "Loans have been imported successfully.")
            return redirect("..")
            
        form = ExcelImportForm(fields=[
            {
                "name": "finance",
                "type": forms.ModelChoiceField,
                "params": {
                "required": True,
                "queryset": Finance.objects.all()
                }
             }])
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"form": form})
        return render(request, "admin/excel_form.html", context)


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "loan_amount",
        "finance",
        "status",
    ]
    
    change_list_template = "admin/cooperative/excel_import_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-users/", self.import_loan_applications),
        ]
        return my_urls + urls

    def import_loan_applications(self, request):
        if request.method == "POST":
            file = request.FILES["excel_file"]
            finance = request.POST.get("finance")
            if finance:
                finance = Finance.objects.get(id=finance)
            imported = import_loan_applications_from_excel(file, finance)
            if not imported:
                self.message_user(request, "Error importing loan applications.")
                return redirect("..")
            self.message_user(request, "Loan applications have been imported successfully.")
            return redirect("..")
            
        form = ExcelImportForm(fields=[
            {
                "name": "finance",
                "type": forms.ModelChoiceField,
                "params": {
                "required": True,
                "queryset": Finance.objects.all()
                }
             }])
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"form": form})
        return render(request, "admin/excel_form.html", context)


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
    change_list_template = "admin/cooperative/excel_import_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-finances/", self.import_finaces),
        ]
        return my_urls + urls

    def import_finaces(self, request):
        if request.method == "POST":
            file = request.FILES["excel_file"]
            imported = import_finance_from_excel(file)
            if not imported:
                self.message_user(request, "Error importing finances.")
                return redirect("..")
            self.message_user(request, "Finances have been imported successfully.")
            return redirect("..")
            
        form = ExcelImportForm()
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"form": form})
        return render(request, "admin/excel_form.html", context)


@admin.register(FinanceStaff)
class FinanceStaffAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "user",
        "finance",
    ]


@admin.register(FinanceUser)
class FinanceUserAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "first_name",
        "last_name",
    ]
    change_list_template = "admin/cooperative/excel_import_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-users/", self.import_users),
        ]
        return my_urls + urls

    def import_users(self, request):
        if request.method == "POST":
            file = request.FILES["excel_file"]
            imported = import_finance_user_from_excel(file)
            if not imported:
                self.message_user(request, "Error importing users.")
                return redirect("..")
            self.message_user(request, "Users have been imported successfully.")
            return redirect("..")
            
        form = ExcelImportForm(fields=[
            {
                "name": "finace",
                "type": forms.CharField,
                "params": {
                "required": True
                }
             }])
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"form": form})
        return render(request, "admin/excel_form.html", context)


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
    change_list_template = "admin/cooperative/excel_import_changelist.html"
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("import-installments/", self.import_installments),
        ]
        return my_urls + urls

    def import_installments(self, request):
        if request.method == "POST":
            file = request.FILES["excel_file"]
            loan = request.POST.get("loan")
            if loan:
                loan = LoanAccount.objects.get(id=loan)
            imported = import_installments_from_excel(file, loan)
            if not imported:
                self.message_user(request, "Error importing installments.")
                return redirect("..")
            self.message_user(request, "Installments have been imported successfully.")
            return redirect("..")
            
        form = ExcelImportForm(fields=[
            {
                "name": "loan",
                "type": forms.ModelChoiceField,
                "params": {
                "required": True,
                "queryset": LoanAccount.objects.all()
                }
             }])
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({"form": form})
        return render(request, "admin/excel_form.html", context)


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
