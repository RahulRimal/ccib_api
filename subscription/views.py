from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from subscription.models import Plan, Subscription
from subscription.serializers import (

    PlanSerializer,
    SubscriptionSerializer,
)


class PlanViewSet(BaseApiMixin, ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    throttle_scope = "plan_api_throttle"


# class PlanCostViewSet(BaseApiMixin, ModelViewSet):
#     queryset = PlanCost.objects.all()
#     serializer_class = PlanCostSerializer


class SubscriptionViewSet(BaseApiMixin, ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    throttle_scope = "subscription_api_throttle"
