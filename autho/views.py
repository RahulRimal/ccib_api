from autho.models import User
from rest_framework.viewsets import ModelViewSet
from common.mixins import BaseApiMixin

from autho.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer

# Create your views here.


class UserViewSet(BaseApiMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserSerializer
