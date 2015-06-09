# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_pesapal', '0002_transaction_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(max_length=16, null=True),
            preserve_default=True,
        ),
    ]
