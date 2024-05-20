from django.urls import path
from . import views as autho_views
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('users', autho_views.UserViewSet, basename='users')


urlpatterns = [
    path("create-token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/",TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", TokenVerifyView.as_view(), name="token_verify"),
]


urlpatterns += router.urls
