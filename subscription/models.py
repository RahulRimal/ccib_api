from django.db import models
from common.models import BaseModelMixin
from django_flex_subscriptions.models import SubscriptionBase, PlanBase
from cooperative.models import Finance


class Plan(BaseModelMixin, PlanBase):
    PERIOD_MONTHLY = "monthly"
    PERIOD_YEARLY = "yearly"
    PERIOD_ONCE = "once"

    PERIOD_CHOICES = [
        (PERIOD_MONTHLY, PERIOD_MONTHLY.capitalize()),
        (PERIOD_YEARLY, PERIOD_YEARLY.capitalize()),
        (PERIOD_ONCE, PERIOD_ONCE.capitalize()),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    period = models.CharField(
        max_length=10, choices=PERIOD_CHOICES, default=PERIOD_YEARLY
    )


class PlanCost(BaseModelMixin):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField()
    recurrence_period = models.DateField()


class Subscription(BaseModelMixin, SubscriptionBase):
    STATUS_ACTIVE = "active"
    STATUS_CANCELLED = "cancelled"
    STATUS_DUE = "due"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, STATUS_ACTIVE.capitalize()),
        (STATUS_CANCELLED, STATUS_CANCELLED.capitalize()),
        (STATUS_DUE, STATUS_DUE.capitalize()),
    ]

    finance = models.ForeignKey(Finance, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    billing_start = models.DateField()
    billing_end = models.DateField()
    last_bill_paid = models.DateField()
    next_billing = models.DateField()
    grace_period = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DUE)
    payment_verified = models.BooleanField(default=False)
    auto_renewable = models.BooleanField(default=True)
