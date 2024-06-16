from django.urls import path
from . import views 

from rest_framework_nested.routers import DefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='users')


urlpatterns = [
    path("create-token/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/",views.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", views.TokenVerifyView.as_view(), name="token_verify"),
]


urlpatterns += router.urls
