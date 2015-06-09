
from django.db import models
from django.utils.translation import ugettext as _

from uuidfield import UUIDField


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
    pesapal_transaction = UUIDField(hyphenate=True)
    merchant_reference = models.IntegerField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)
    payment_status = models.IntegerField(choices=TRANSACTION_STATUS, default=PENDING)
    payment_method = models.CharField(max_length=16, null=True)

    class Meta:
        unique_together = (('merchant_reference', 'pesapal_transaction'),)

    def __unicode__(self):
        return u'Transaction: {0}, Merchant_Reference: {1}'.format(self.pesapal_transaction, self.merchant_reference)
