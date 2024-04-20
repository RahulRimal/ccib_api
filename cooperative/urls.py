from django.urls import path
from. import views

# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

urlpatterns = router.urls