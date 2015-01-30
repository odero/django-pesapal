from django.db import models

class BaseTransaction(models.Model):
    pesapal_transaction_id = models.CharField(max_length=32, null=True, blank=True, unique=True)
    pesapal_merchant_reference = models.IntegerField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    currency = models.CharField(max_length=8, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    PENDING, COMPLETED, FAILED, INVALID = 'PENDING', 'COMPLETED', 'FAILED', 'INVALID'

    status = models.CharField(max_length=16)

    class Meta:
        unique_together = (('pesapal_transaction_id', 'pesapal_merchant_reference'),)
        abstract = True

    def __unicode__(self):
        return u'Transaction: {0}, Campaign_id: {1}'.format(self.pesapal_transaction_id, self.pesapal_merchant_reference)
