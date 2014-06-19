from django.db import models
from uuidfield import UUIDField


class Transaction(models.Model):
    transaction_id = UUIDField()
    merchant_reference = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'Transaction: {0}, Campaign_id: {1}'.format(self.transaction_id, self.merchant_reference)
