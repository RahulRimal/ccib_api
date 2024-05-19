from autho.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from common.mixins import BaseApiMixin

from autho.serializers import UserSerializer

# Create your views here.


class UserViewSet(BaseApiMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer




class TokenObtainPairView(TokenObtainPairView):
    # permission_classes = ([BazraPermission])
    pass


class TokenRefreshView(TokenRefreshView):
    # permission_classes = ([BazraPermission])
    pass


class TokenVerifyView(TokenVerifyView):
    # permission_classes = ([BazraPermission])
    pass


