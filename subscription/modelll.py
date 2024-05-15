# from django.db import models

# from common.models import BaseModelMixin

# # Create your models here.


# class Plan(BaseModelMixin):

#     PERIOD_MONTHLY = "monthly"
#     PERIOD_YEARLY = "yearly"

#     PERIOD_CHOICES = [
#         (PERIOD_MONTHLY, PERIOD_MONTHLY.capitalize()),
#         (PERIOD_YEARLY, PERIOD_YEARLY.capitalize()),
#     ]

#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     period = models.CharField(
#         max_length=10, choices=PERIOD_CHOICES, default=PERIOD_YEARLY
#     )


# class PlanCost(BaseModelMixin):
#     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     cost = models.PositiveIntegerField(max_digits=8)
#     recurrance = models.DateField()


# class Subscription(BaseModelMixin):

#     STATUS_ACTIVE = "active"
#     STATUS_CANCELLED = "cancelled"
#     STATUS_DUE = "due"

#     STATUS_CHOICES = [
#         (STATUS_ACTIVE, STATUS_ACTIVE.capitalize()),
#         (STATUS_CANCELLED, STATUS_CANCELLED.capitalize()),
#         (STATUS_DUE, STATUS_DUE.capitalize()),
#     ]
#     finance = models.ForeignKey("cooperative.Finance", on_delete=models.CASCADE)
#     plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
#     billing_start = models.DateTimeField()
#     billing_end = models.DateTimeField()
#     last_bill_paid = models.DateTimeField()
#     next_billing = models.DateTimeField()
#     grace_period = models.PositiveIntegerField(default=0)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DUE)
#     verified = models.BooleanField(default=False)
#     auto_renewable = models.BooleanField(default=True)
