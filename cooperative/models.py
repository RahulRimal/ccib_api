from django.db import models
from autho.models import User

from common.models import BaseModelMixin


# PersonalGuarantor model
class PersonalGuarantor(BaseModelMixin):
    user = models.ForeignKey(User, on_delete=models.PROTECT)


# Loan model
class Loan(BaseModelMixin):
    DUE_TYPE_DAILY = "d"
    DUE_TYPE_MONTHLY = "m"
    DUE_TYPE_QUARTERLY = "q"
    DUE_TYPE_YEARLY = "y"

    INSTALLMENT_DUE_TYPE_CHOICES = [
        (DUE_TYPE_DAILY, "Daily"),
        (DUE_TYPE_MONTHLY, "Monthly"),
        (DUE_TYPE_QUARTERLY, "Quarterly"),
        (DUE_TYPE_YEARLY, "Yearly"),
    ]

    # Nature type choices
    NATURE_TERM = "term"
    NATURE_OVERDRAFT = "overdraft"

    NATURE_CHOICES = [
        (NATURE_TERM, "Term"),
        (NATURE_OVERDRAFT, "Overdraft (OD)"),
    ]

    name = models.CharField(max_length=100)
    nature = models.CharField(max_length=25, choices=NATURE_CHOICES, default=NATURE_TERM)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    maturity_date = models.DateField()
    installment_due_type = models.CharField(
        max_length=1, choices=INSTALLMENT_DUE_TYPE_CHOICES, default=DUE_TYPE_DAILY
    )
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currently_outstanding = models.DecimalField(max_digits=12, decimal_places=2)
    total_due = models.DecimalField(max_digits=12, decimal_places=2)
    personal_guarantors = models.ManyToManyField(
        PersonalGuarantor, related_name="guaranted_loans", blank=True
    )


LONE_TAKER_PERSON = "personal"
LONE_TAKER_COMPANY = "company"

# Choices for lone taker type
LONE_TAKER_TYPE_CHOICES = [
    (LONE_TAKER_PERSON, "Person"),
    (LONE_TAKER_COMPANY, "Company"),
]


class Company(BaseModelMixin):

    LONE_TAKER_PERSON = "personal"
    LONE_TAKER_COMPANY = "company"

    # Choices for lone taker type
    LONE_TAKER_TYPE_CHOICES = [
        (LONE_TAKER_PERSON, "Personal"),
        (LONE_TAKER_COMPANY, "Company"),
    ]

    name = models.CharField(max_length=255)
    pan_num = models.CharField(max_length=9, blank=True, null=True)
    vat_num = models.CharField(max_length=9, blank=True, null=True)
    permanent_add = models.CharField(max_length=255)
    pan_registration_date = models.DateField(blank=True, null=True)
    pan_registration_place = models.CharField(max_length=100, blank=True, null=True)
    share_holders = models.ManyToManyField(User, related_name="companies", blank=True)
    if_profiter_then_no_shareholders = models.CharField(
        max_length=100, blank=True, null=True
    )
    profiter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lone_taker_type = models.CharField(
        max_length=10, choices=LONE_TAKER_TYPE_CHOICES, default=LONE_TAKER_COMPANY
    )

    def __str__(self):
        return self.name
