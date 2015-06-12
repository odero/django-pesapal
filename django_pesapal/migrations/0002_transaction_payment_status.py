# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_pesapal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_status',
            field=models.IntegerField(default=0, choices=[(0, 'Pending'), (1, 'Completed'), (2, 'Failed')]),
            preserve_default=True,
        ),
    ]
