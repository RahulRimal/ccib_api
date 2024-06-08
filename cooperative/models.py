from django.db import models
from autho.models import StaffUser, User

from common.models import BaseModelMixin


# PersonalGuarantor model
class PersonalGuarantor(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    loan = models.ForeignKey(
        "LoanAccount", on_delete=models.CASCADE, related_name="personal_guarantors"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class LoanAccount(BaseModelMixin):
    STATUS_GOOD = "good"
    STATUS_WATCHLIST = "watchlist"
    STATUS_PASS = "pass"
    # npl = non_performing_loan
    STATUS_NPL = "npl"
    STATUS_DOUBTFUL = "doubtful"
    STATUS_BAD_DEBT = "bad debt"

    STATUS_CHOICES = [
        (STATUS_GOOD, STATUS_GOOD.capitalize()),
        (STATUS_WATCHLIST, STATUS_WATCHLIST.capitalize()),
        (STATUS_PASS, STATUS_PASS.capitalize()),
        (STATUS_NPL, STATUS_NPL.capitalize()),
        (STATUS_DOUBTFUL, STATUS_DOUBTFUL.capitalize()),
        (STATUS_BAD_DEBT, STATUS_BAD_DEBT.capitalize()),
    ]

    NATURE_TERM = "term"
    NATURE_OVERDRAFT = "overdraft"

    NATURE_CHOICES = [
        (NATURE_TERM, NATURE_TERM.capitalize()),
        (NATURE_OVERDRAFT, NATURE_OVERDRAFT.capitalize()),
    ]

    INSTALLMENT_DUE_TYPE_DAILY = "daily"
    INSTALLMENT_DUE_TYPE_WEEKLY = "weekly"
    INSTALLMENT_DUE_TYPE_MONTHLY = "monthly"
    INSTALLMENT_DUE_TYPE_YEARLY = "yearly"
    INSTALLMENT_DUE_TYPE_CHOICES = [
        (INSTALLMENT_DUE_TYPE_DAILY, INSTALLMENT_DUE_TYPE_DAILY.capitalize()),
        (INSTALLMENT_DUE_TYPE_WEEKLY, INSTALLMENT_DUE_TYPE_WEEKLY.capitalize()),
        (INSTALLMENT_DUE_TYPE_MONTHLY, INSTALLMENT_DUE_TYPE_MONTHLY.capitalize()),
        (INSTALLMENT_DUE_TYPE_YEARLY, INSTALLMENT_DUE_TYPE_YEARLY.capitalize()),
    ]

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    finance = models.ForeignKey(
        "Finance", on_delete=models.CASCADE, related_name="loans"
    )
    account_number = models.CharField(max_length=20, unique=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_due_type = models.CharField(
        max_length=20,
        choices=INSTALLMENT_DUE_TYPE_CHOICES,
        default=INSTALLMENT_DUE_TYPE_DAILY,
    )
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_outstanding = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    overdue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_GOOD
    )
    loan_nature = models.CharField(
        max_length=20, choices=NATURE_CHOICES, default=NATURE_TERM
    )
    is_closed = models.BooleanField(default=False)
    utilization_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    maturity_date = models.DateField()

    def save(self, *args, **kwargs):
        if self.pk is None and self.loan_limit == 0:
            self.loan_limit = self.loan_amount

        self.total_outstanding = self.loan_amount - self.total_paid
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_number


class Installment(BaseModelMixin):
    loan = models.ForeignKey(
        LoanAccount, on_delete=models.CASCADE, related_name="installments"
    )
    due_date = models.DateField()
    paid_date = models.DateField()
    total_due = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_outstanding = models.DecimalField(max_digits=10, decimal_places=2)


class Company(BaseModelMixin):

    LONE_TAKER_PERSON = "personal"
    LONE_TAKER_COMPANY = "company"

    # Choices for lone taker type
    LONE_TAKER_TYPE_CHOICES = [
        (LONE_TAKER_PERSON, LONE_TAKER_PERSON.capitalize()),
        (LONE_TAKER_COMPANY, LONE_TAKER_COMPANY.capitalize()),
    ]

    name = models.CharField(max_length=255)
    pan_num = models.CharField(max_length=9, blank=True, null=True)
    vat_num = models.CharField(max_length=9, blank=True, null=True)
    permanent_add = models.CharField(max_length=255)
    pan_registration_date = models.DateField(blank=True, null=True)
    pan_registration_place = models.CharField(max_length=100, blank=True, null=True)
    profiter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lone_taker_type = models.CharField(
        max_length=10, choices=LONE_TAKER_TYPE_CHOICES, default=LONE_TAKER_COMPANY
    )

    def __str__(self):
        return self.name

    def has_read_permission(self):
        return True


class Shareholder(BaseModelMixin):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="share_holders"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Finance(BaseModelMixin):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("Finance", on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=1000)
    location = models.JSONField(default=dict)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    website_url = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.name


class FinanceStaff(BaseModelMixin):
    user = models.OneToOneField(StaffUser, on_delete=models.CASCADE, related_name="finance_staff")
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name="staffs")    


class LoanApplication(BaseModelMixin):

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING.capitalize()),
        (STATUS_APPROVED, STATUS_APPROVED.capitalize()),
        (STATUS_REJECTED, STATUS_REJECTED.capitalize()),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="loan_applications"
    )
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    finance = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name="loan_applications"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )


class SecurityDeposit(BaseModelMixin):
    TYPE_REAL_ESTATE = "real state"
    TYPE_FIXED_ASSET = "fixed asset"
    TYPE_HIGHER_PURCHASE = "higher purchase"

    TYPE_CHOICES = [
        (TYPE_REAL_ESTATE, TYPE_REAL_ESTATE.capitalize()),
        (TYPE_FIXED_ASSET, TYPE_FIXED_ASSET.capitalize()),
        (TYPE_HIGHER_PURCHASE, TYPE_HIGHER_PURCHASE.capitalize()),
    ]

    OWNERSHIP_OWN = "own"
    OWNERSHIP_THIRD_PARTY = "third party"

    OWNERSHIP_CHOICES = [
        (OWNERSHIP_OWN, OWNERSHIP_OWN.capitalize()),
        (OWNERSHIP_THIRD_PARTY, OWNERSHIP_THIRD_PARTY.capitalize()),
    ]

    NATURE_FIRST_CHARGE = "first_charge"

    loan = models.ForeignKey(
        LoanAccount, on_delete=models.CASCADE, related_name="securities"
    )
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_REAL_ESTATE
    )
    description = models.TextField()
    ownership_type = models.CharField(
        max_length=20, choices=OWNERSHIP_CHOICES, default=OWNERSHIP_OWN
    )
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    nature_of_charge = models.CharField(
        max_length=20, default=NATURE_FIRST_CHARGE, editable=False
    )
    latest_value = models.DecimalField(max_digits=15, decimal_places=2)
    latest_valuation_date = models.DateField()

    def __str__(self):
        return self.description


class Blacklist(BaseModelMixin):
    CATEGORY_BORROWER = "borrower"
    CATEGORY_GUARANTOR = "guarantor"

    CATEGORY_CHOICES = [
        (CATEGORY_BORROWER, CATEGORY_BORROWER.capitalize()),
        (CATEGORY_GUARANTOR, CATEGORY_GUARANTOR.capitalize()),
    ]

    STATUS_BLACKLISTED = "blacklisted"
    STATUS_RELISHED = "relished"

    STATUS_CHOICES = [
        (STATUS_BLACKLISTED, STATUS_BLACKLISTED.capitalize()),
        (STATUS_RELISHED, STATUS_RELISHED.capitalize()),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="black_list")
    finance = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name="black_list"
    )
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_BORROWER
    )
    reason = models.CharField(max_length=500)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_BLACKLISTED
    )
    release_date = models.DateField(null=True, blank=True)
    report_date = models.DateField()


class BlacklistReport(BaseModelMixin):
    STATUS_PROGRESS = "progress"
    STATUS_REJECTED = "rejected"
    STATUS_APPROVED = "approved"

    STATUS_CHOICES = [
        (STATUS_PROGRESS, STATUS_PROGRESS.capitalize()),
        (STATUS_REJECTED, STATUS_REJECTED.capitalize()),
        (STATUS_APPROVED, STATUS_APPROVED.capitalize()),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="black_list_reports"
    )
    finance = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name="black_list_reports"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PROGRESS
    )


class Inquiry(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    finance = models.ForeignKey(
        Finance, on_delete=models.CASCADE, related_name="inquiries"
    )
    reason = models.CharField(max_length=500)
    inquirer = models.ForeignKey(
        StaffUser, on_delete=models.PROTECT, related_name="inquiries"
    )
