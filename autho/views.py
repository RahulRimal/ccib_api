from django.http import HttpRequest
from autho.models import User
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from common.api_response import api_response_error, api_response_success
from common.mixins import BaseApiMixin

from autho.serializers import UserSerializer

# Create your views here.


class UserViewSet(BaseApiMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(detail=False, methods = ['GET', 'PATCH'])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    # def me(self, request):
    #     user = User.objects.get(
    #         id=request.user.id)
    #     if request.method == 'GET':
    #         serializer = UserSerializer(user)
    #         return Response(serializer.data)
    #     elif request.method == 'PATCH':
    #         serializer = UserSerializer(user, data=request.data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)
    

   


class TokenObtainPairView(TokenObtainPairView):
    # permission_classes = ([BazraPermission])
    pass


class TokenRefreshView(TokenRefreshView):
    # permission_classes = ([BazraPermission])
    pass


class TokenVerifyView(TokenVerifyView):
    # permission_classes = ([BazraPermission])
    pass

