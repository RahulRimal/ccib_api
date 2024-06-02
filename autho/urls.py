from django.urls import path
from . import views 

# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='users')
router.register('staffusers', views.StaffUserViewSet, basename='staffusers')


urlpatterns = [
    path("create-token/", views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/",views.TokenRefreshView.as_view(), name="token_refresh"),
    path("verify-token/", views.TokenVerifyView.as_view(), name="token_verify"),
]


urlpatterns += router.urls
