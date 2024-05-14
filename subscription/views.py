from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from subscription.models import Plan, PlanCost, Subscription
from subscription.serializers import (
    PlanCostSerializer,
    PlanSerializer,
    SubscriptionSerializer,
)


class PlanViewSet(BaseApiMixin, ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class PlanCostViewSet(BaseApiMixin, ModelViewSet):
    queryset = PlanCost.objects.all()
    serializer_class = PlanCostSerializer


class SubscriptionViewSet(BaseApiMixin, ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
