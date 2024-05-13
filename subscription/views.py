from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from common.mixins import BaseApiMixin
from subscription.models import Plan, PlanCost, Subscription
from subscription.serializers import CreatePlanCostSerializer, CreatePlanSerializer, PlanCostSerializer, PlanSerializer, SubscriptionSerializer, UpdatePlanCostSerializer, UpdatePlanSerializer

# Create your views here.


class PlanViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Plan.objects.all()
    # serializer_class = PlanSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePlanSerializer
        if self.request.method == "PATCH":
            return UpdatePlanSerializer
        return PlanSerializer

class PlanCostViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = PlanCost.objects.all()
    # serializer_class = PlanCostSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreatePlanCostSerializer
        if self.request.method == "PATCH":
            return UpdatePlanCostSerializer
        return PlanCostSerializer

class SubscriptionViewSet(BaseApiMixin, ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

