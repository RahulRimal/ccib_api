from django.urls import path
from. import views

from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register('plans', views.PlanViewSet, basename='plans')
router.register('subscriptions', views.SubscriptionViewSet, basename='subscriptions')
router.register('plan_costs', views.PlanCostViewSet, basename='plan_costs')


urlpatterns = router.urls 