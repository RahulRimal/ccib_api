from autho.models import User
from rest_framework.viewsets import ModelViewSet

from autho.serializers import UserSerializer

# Create your views here.


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
