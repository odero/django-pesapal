
from __future__ import absolute_import, unicode_literals

import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Transaction(models.Model):

    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    INVALID = 3

    TRANSACTION_STATUS = (
        (PENDING, _('Pending')),
        (COMPLETED, _('Completed')),
        (FAILED, _('Failed')),
    )
    pesapal_transaction = models.UUIDField(
        default=uuid.uuid4, editable=False)
    merchant_reference = models.IntegerField(db_index=True)
    amount = models.DecimalField(
        decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)
    payment_status = models.IntegerField(
        choices=TRANSACTION_STATUS, default=PENDING)
    payment_method = models.CharField(max_length=24, null=True)

    class Meta:
        unique_together = (('merchant_reference', 'pesapal_transaction'),)

    def __str__(self):
        return 'Transaction: {0}, Merchant_Reference: {1}'.format(
            self.pesapal_transaction, self.merchant_reference)
