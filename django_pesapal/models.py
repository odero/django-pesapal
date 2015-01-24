from django.db import models


class BaseTransaction(models.Model):
    pesapal_transaction_id = models.CharField(max_length=32, null=True, blank=True, unique=True)
    merchant_reference = models.IntegerField(db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('merchant_reference', 'pesapal_transaction'),)
        abstract = True

    def __unicode__(self):
        return u'Transaction: {0}, Campaign_id: {1}'.format(self.pesapal_transaction, self.merchant_reference)
