from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from subscription.models import Plan, Subscription
from subscription.serializers import (

    PlanSerializer,
    SubscriptionSerializer,
)


class PlanViewSet(BaseApiMixin, ModelViewSet):
    """Get , update , create and delete plan details"""
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


# class PlanCostViewSet(BaseApiMixin, ModelViewSet):
#     queryset = PlanCost.objects.all()
#     serializer_class = PlanCostSerializer


class SubscriptionViewSet(BaseApiMixin, ModelViewSet):
    """Get , update , create and delete subscription details by the Finance idx and the Plan idx"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
