# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_pesapal', '0003_transaction_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='pesapal_transaction',
            field=models.UUIDField(default=uuid.uuid4, editable=False, name='pesapal_transaction'),
            preserve_default=True,
        ),
    ]
