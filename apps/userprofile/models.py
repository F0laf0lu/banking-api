from typing import Any

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedModel

User = get_user_model()

class Profile(TimeStampedModel):

    class Gender(models.TextChoices):
        MALE = (
            "male",
            _("Male"),
        )
        FEMALE = (
            "female",
            _("Female"),
        )

    class MaritalStatus(models.TextChoices):
        MARRIED = (
            "married",
            _("Married"),
        )
        SINGLE = (
            "single",
            _("Single"),
        )
        DIVORCED = (
            "divorced",
            _("Divorced"),
        )
        WIDOWED = (
            "widowed",
            _("Widowed"),
        )
        SEPARATED = (
            "separated",
            _("Separated"),
        )
        UNKNOWN = (
            "unknown",
            _("Unknown"),
        )
    class EmploymentStatus(models.TextChoices):
        SELF_EMPLOYED = (
            "self_employed",
            _("Self Employed"),
        )
        EMPLOYED = (
            "employed",
            _("Employed"),
        )
        UN_EMPLOYED = (
            "unemployed",
            _("Unemployed"),
        )
        RETIRED = (
            "retired",
            _("Retired"),
        )
        STUDENT = (
            "student",
            _("Student"),
        )

    # Basic profile info
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(_("Gender"), max_length=8, choices=Gender.choices, default=Gender.MALE)
    phone_number = PhoneNumberField(_("Phone Number"), max_length=30, default=settings.DEFAULT_PHONE_NUMBER)
    address = models.CharField(_("Address"), max_length=100,  default="Unknown")
    city = models.CharField(_("City"), max_length=50,  default="Unknown")
    country = CountryField(_("Country"), default=settings.DEFAULT_COUNTRY)
    date_of_birth = models.DateField(_("Date of Birth"), default=settings.DEFAULT_BIRTH_DATE)

    # Marital Status
    marital_status = models.CharField(_("Marital Status"),max_length=20,choices=MaritalStatus.choices, default=MaritalStatus.UNKNOWN)


    # Employment Info
    employment_status = models.CharField(
        _("Employment Status"),
        max_length=20,
        choices=EmploymentStatus.choices,
        default=EmploymentStatus.SELF_EMPLOYED,
    )
    employer_name = models.CharField(
        _("Employer Name"),
        max_length=50,
        blank=True,
        null=True,
    )
    annual_income = models.DecimalField(
        _("Annual Income"),
        max_digits=12,
        decimal_places=2,
        default=0.0,
    )
    
    date_of_employment = models.DateField(
        _("Date of Employment"),
        blank=True,
        null=True,
    )
    employer_address = models.CharField(
        _("Employer Address"),
        max_length=100,
        blank=True,
        null=True,
    )
    employer_city = models.CharField(
        _("Employer City"),
        max_length=50,
        blank=True,
        null=True,
    )
    employer_state = models.CharField(
        _("Employer State"),
        max_length=50,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"