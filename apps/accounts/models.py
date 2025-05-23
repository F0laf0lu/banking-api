from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from decimal import Decimal, ROUND_HALF_UP
from loguru import logger

User = get_user_model()


class BankAccount(TimeStampedModel):
    class AccountType(models.TextChoices):
        CURRENT = ("current", _("Current"))
        SAVINGS = ("savings", _("Savings"))

    class AccountStatus(models.TextChoices):
        ACTIVE = ("active", _("Active"))
        INACTIVE = ("in-active", _("In-active"))

    class AccountCurrency(models.TextChoices):
        DOLLAR = ("us_dollar", _("US Dollar"))
        POUND_STERLING = ("pound_sterling", _("Pound Sterling"))
        NAIRA = ("naira", _("Naira"))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bank_accounts"
    )

    account_number = models.CharField(_("Account Number"), max_length=20, unique=True)
    account_balance = models.DecimalField(
        _("Account Balance"), decimal_places=2, max_digits=10, default=0.00
    )
    currency = models.CharField(
        _("Currency"), max_length=20, choices=AccountCurrency.choices
    )
    account_status = models.CharField(
        _("Account Status"),
        max_length=10,
        choices=AccountStatus.choices,
        default=AccountStatus.INACTIVE,
    )
    account_type = models.CharField(
        _("Account Type"),
        max_length=20,
        choices=AccountType.choices,
    )


    def __str__(self) -> str:
        return (
            f"{self.user.full_name}'s {self.get_currency_display()} - "
            f"{self.get_account_type_display()} Account - {self.account_number} "
        )
    
    class Meta:
        verbose_name = _("Bank Account")
        verbose_name_plural = _("Bank Accounts")
        unique_together = ["user", "currency", "account_type"]

    def clean(self):
        if self.account_balance < 0:
            raise ValidationError(_("Account balance cannot be negative."))


class Transaction(TimeStampedModel):
    class TransactionStatus(models.TextChoices):
        PENDING = ("pending", _("Pending"))
        COMPLETED = ("completed", _("Completed"))
        FAILED = ("failed", _("Failed"))

    class TransactionType(models.TextChoices):
        DEPOSIT = ("deposit", _("Deposit"))
        WITHDRAWAL = ("withdrawal", _("Withdrawal"))
        TRANSFER = ("transfer", _("Transfer"))
        INTEREST = ("interest", _("Interest"))

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="transactions"
    )
    amount = models.DecimalField(
        _("Amount"), decimal_places=2, max_digits=12, default=0.00
    )
    description = models.CharField(
        _("Description"), max_length=500, null=True, blank=True
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_transactions",
    )
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sent_transactions"
    )

    receiver_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_transactions",
    )
    sender_account = models.ForeignKey(
        BankAccount,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_transactions",
    )
    status = models.CharField(
        choices=TransactionStatus.choices,
        max_length=20,
        default=TransactionStatus.PENDING,
    )
    transaction_type = models.CharField(choices=TransactionType.choices, max_length=20)

    def __str__(self) -> str:
        return f"{self.transaction_type} - {self.amount} - {self.status}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["created_at"])]