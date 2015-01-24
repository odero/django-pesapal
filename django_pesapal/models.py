from django.db import models

from uuidfield import UUIDField


class BaseTransaction(models.Model):
    pesapal_transaction_id = UUIDField(hyphenate=True)
    pesapal_merchant_reference = models.IntegerField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('merchant_reference', 'pesapal_transaction'),)
        abstract = True

    def __unicode__(self):
        return u'Transaction: {0}, Campaign_id: {1}'.format(self.pesapal_transaction, self.merchant_reference)
