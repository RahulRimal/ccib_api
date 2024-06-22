import datetime
import logging
from rest_framework import serializers

from cooperative.serializers import FinanceSerializer
from common.mixins import DetailRelatedField, BaseModelSerializerMixin
from cooperative.models import Finance
from subscription.models import Plan, Subscription


logger = logging.getLogger(__name__)
# class PlanCostSerializer(BaseModelSerializerMixin):
#     class Meta:
#         model = PlanCost
#         fields = ["idx", "price"]


class PlanSerializer(BaseModelSerializerMixin):
    class Meta:
        model = Plan
        fields = ["idx", "name", "description", "period", "price", "is_active"]


class SubscriptionSerializer(BaseModelSerializerMixin):
    plan_idx = serializers.CharField(write_only=True)
    finance_idx = serializers.CharField(write_only=True)
    finance = FinanceSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)



    class Meta:
        model = Subscription
        fields = [
            "idx",
            "plan_idx",
            "finance_idx",
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

    def create(self, validated_data):
        try:
            finance = Finance.objects.get(idx=validated_data.pop("finance_idx"))
        except Finance.DoesNotExist:
            logger.warning("Finance does not exist: %s", validated_data["finance_idx"])
            raise serializers.ValidationError("Finance does not exist")
        validated_data["finance"] = finance
        try:
            plan = Plan.objects.get(idx=validated_data.pop("plan_idx"))
        except Plan.DoesNotExist:
            logger.warning("Plan does not exist: %s", validated_data["plan_idx"])
            raise serializers.ValidationError("Plan does not exist")
        validated_data["plan"] = plan
        validated_data["recurrance_period"] = Subscription.get_recurrance_period(plan.period, validated_data["billing_start"])
        return super().create(validated_data)
    
   
    




     


    

