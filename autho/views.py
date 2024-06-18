from django.http import HttpRequest

from autho.models import User, User
from django.db.models import Count

from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from autho.permission import CCIBPermission
from common.api_response import api_response_error, api_response_success
from common.mixins import BaseApiMixin
from autho.serializers import UserSerializer, UserSerializer
from cooperative.models import LoanAccount
from cooperative.serializers import FinanceSerializer


class UserViewSet(BaseApiMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["GET", "PATCH"])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def change_password(self, request: HttpRequest, *args, **kwargs) -> Response:

        if not request.user.is_authenticated:
            return api_response_error(
                {"detail": "User is not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user: User = self.get_object()

        requesting_user: User = request.user

        if requesting_user != user:
            return api_response_error(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        is_correct = user.check_password(old_password)
        if is_correct:
            if not new_password:
                return api_response_error(
                    {"detail": "New password cannot be empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
            user.save()
            return api_response_success(
                {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
            )
        else:
            return api_response_error(
                {"detail": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TokenObtainPairView(TokenObtainPairView):
    permission_classes = [CCIBPermission]


class TokenRefreshView(TokenRefreshView):
    # permission_classes = ([BazraPermission])
    pass


class TokenVerifyView(TokenVerifyView):
    # permission_classes = ([BazraPermission])
    pass
