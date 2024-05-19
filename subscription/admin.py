from django.contrib import admin

from subscription.models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["idx", "name", "description", "period", "price", "is_active"]


# @admin.register(PlanCost)
# class PlanCostAdmin(admin.ModelAdmin):
#     list_display = ["idx", "price"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "idx",
        "finance",
        "plan",
        "billing_start",
        "billing_end",
        "last_bill_paid",
        "next_billing",
        "grace_period",
        "status",
        "is_payment_verified",
        "is_auto_renewable",
        "recurrance_period",
    ]
