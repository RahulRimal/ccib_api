from autho.models import User
from rest_framework.viewsets import ModelViewSet
from common.mixins import BaseApiMixin

from autho.serializers import UserSerializer

# Create your views here.


class UserViewSet(BaseApiMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer