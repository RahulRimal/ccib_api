from common.mixins import BaseModelSerializerMixin
from subscription.models import Plan, PlanCost, Subscription


class PlanSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Plan
        fields = ["idx", "name", "description", "period"]


class PlanCostSerializer(BaseModelSerializerMixin):
    class Meta:
        model = PlanCost
        fields = ["idx", "plan", "cost", "recurrance"]


class SubscriptionSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Subscription
        fields = [
            "idx",
            "finance",
            "plan",
            "billing_start",
            "billing_end",
            "last_bill_paid",
            "next_billing",
            "grace_period",
            "status",
            "verified",
            "auto_renewable",
        ]
