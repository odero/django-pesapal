# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('django_pesapal', '0003_transaction_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='pesapal_transaction',
            field=uuidfield.fields.UUIDField(hyphenate=True, name='pesapal_transaction'),
            preserve_default=True,
        ),
    ]
