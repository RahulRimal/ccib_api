import datetime
from datetime import timedelta
from functools import cached_property

from django.http import HttpRequest
from django.db import models
from django.db.models import F, ExpressionWrapper, BooleanField, DateTimeField
from django.db.models.functions import Now
from django.db.models import Case, When
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    AbstractUser
)
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.helpers import get_local_date
from common.models import BaseModelMixin


class User(BaseModelMixin, AbstractUser):

    @cached_property
    def is_finance_staff(self) -> bool:
        from cooperative.models import FinanceStaff
        return FinanceStaff.objects.filter(user=self).exists()

    @staticmethod
    def has_write_permission(request: HttpRequest) -> bool:
        """
        Check if the user has write permission.

        Args:
            request (HttpRequest): The request object.

        Returns:
            bool: Whether the user has write permission.
        """
        from cooperative.models import FinanceStaff
        from subscription.models import Subscription
        
        # Check permission for login api
        if request.path == "/auth/create-token/":
            user: User = authenticate(
                request,
                username=request.data.get("username"),
                password=request.data.get("password"),
            )
            if not user:
                return False

            if user.is_superuser:
                return True

            finance_staff: FinanceStaff = FinanceStaff.objects.filter(user=user).first()

            if finance_staff:
                active_subscription: Subscription = Subscription.objects.filter(
                    finance=finance_staff.finance, status="active"
                ).first()

                if active_subscription:
                    return True

                grace_subscription: Subscription = (
                    Subscription.objects.filter(
                        finance=finance_staff.finance, status="due"
                    )
                    .annotate(
                        grace_end_date=ExpressionWrapper(
                            F("next_billing") + F("grace_period") ,
                            output_field=DateTimeField(),
                        ),
                        is_grace_remaining=Case(
                            When(grace_end_date__gte=get_local_date(), then=True),
                            default=False,
                            output_field=BooleanField(),
                        ),
                    )
                    .first()
                )

                return grace_subscription and grace_subscription.is_grace_remaining

            return False

        return False