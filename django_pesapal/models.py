import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Transaction(models.Model):

    INVALID = 0  # in v3 == INVALID
    COMPLETED = 1
    FAILED = 2
    REVERSED = 3  # in v3 == REVERSED
    PENDING = 999

    TRANSACTION_STATUS = (
        (PENDING, _("Invalid")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
        (REVERSED, _("Reversed")),
        (PENDING, _("Pending")),
    )

    pesapal_transaction = models.UUIDField(default=uuid.uuid4, editable=False)
    merchant_reference = models.CharField(max_length=255, db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)
    payment_status = models.IntegerField(choices=TRANSACTION_STATUS, default=PENDING)
    payment_method = models.CharField(max_length=24, null=True)
    payment_account = models.CharField(max_length=64, default="")

    class Meta:
        unique_together = (("merchant_reference", "pesapal_transaction"),)

    def __str__(self):
        return "Transaction: {0}, Merchant_Reference: {1}".format(
            self.pesapal_transaction,
            self.merchant_reference,
        )
