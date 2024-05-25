from django.db import models
from autho.models import User

from common.models import BaseModelMixin


# PersonalGuarantor model
class PersonalGuarantor(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    loan = models.ForeignKey(
        "Loan", on_delete=models.CASCADE, related_name="personal_guarantors"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"



class Loan(BaseModelMixin):
    STATUS_GOOD = "good"
    STATUS_WATCHLIST = "watchlist"
    STATUS_PASS = "pass"
    STATUS_NPL = "npl"
    STATUS_DOUBTFUL = "doubtful"
    STATUS_BAD_DEBT = "bad Debt"

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    account_number = models.CharField(max_length=20, unique=True)
    total_loan = models.DecimalField(max_digits=10, decimal_places=2)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    loan_outstanding = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    loan_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    overdue_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_GOOD)
    loan_type = models.CharField(max_length=20, choices=NATURE_CHOICES, default=NATURE_TERM)
    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None and self.loan_limit == 0:
         self.loan_limit = self.total_loan

        self.loan_outstanding = self.total_loan - self.total_paid
        super().save(*args, **kwargs)


    def __str__(self):
        return self.account_number
    

class Installment(BaseModelMixin):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="installments")
    due_date = models.DateField()
    paid_date = models.DateField()
    total_due = models.DecimalField(max_digits=10, decimal_places=2)
    over_paid = models.DecimalField(max_digits=10, decimal_places=2)
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
    description = models.CharField(max_length=1000)
    location = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class LoanApplication(BaseModelMixin):

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_applications")
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE, related_name="loan_applications")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)



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

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="securities")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_REAL_ESTATE)
    description = models.TextField()
    ownership_type = models.CharField(max_length=20, choices=OWNERSHIP_CHOICES, default=OWNERSHIP_OWN)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    nature_of_charge = models.CharField(max_length=20, default=NATURE_FIRST_CHARGE, editable=False)
    latest_value = models.DecimalField(max_digits=15, decimal_places=2)
    latest_valuation_date = models.DateField()

    def __str__(self):
        return self.description


