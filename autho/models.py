import datetime
from datetime import timedelta

from django.http import HttpRequest
from django.db import models
from django.db.models import F, ExpressionWrapper, BooleanField, DateTimeField
from django.db.models.functions import Now
from django.db.models import Case, When
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager as BaseUserManager,
)
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.helpers import get_local_date
from common.models import BaseModelMixin


class StaffUserManager(BaseUserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        extra_fields.setdefault("citizenship_number", "")
        extra_fields.setdefault("citizenship_issued_place", "")
        extra_fields.setdefault("citizenship_issued_date", datetime.date.today())
        extra_fields.setdefault("father_name", "")

        return self._create_user(username, email, password, **extra_fields)


class User(BaseModelMixin):
    """
    Username and password are required. Other fields are optional.
    """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = (
        (GENDER_MALE, GENDER_MALE.capitalize()),
        (GENDER_FEMALE, GENDER_FEMALE.capitalize()),
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    citizenship_number = models.CharField(max_length=50)
    citizenship_issued_place = models.CharField(max_length=255)
    citizenship_issued_date = models.DateField()
    gender = models.CharField(
        _("gender"), max_length=10, choices=GENDER_CHOICES, default=GENDER_MALE
    )
    dob = models.DateField(blank=True, null=True)
    father_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    grandfather_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    permanent_address = models.CharField(max_length=255)
    temporary_address = models.CharField(max_length=255)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @staticmethod
    def has_list_permission(request: HttpRequest, *args, **kwargs):
        return request.user.is_authenticated

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class StaffUser(AbstractBaseUser, PermissionsMixin, User):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    objects = StaffUserManager()

    USERNAME_FIELD = "username"

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
            user: StaffUser = authenticate(
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
