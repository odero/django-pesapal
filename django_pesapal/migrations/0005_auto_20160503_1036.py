# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_pesapal', '0004_auto_20150812_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(max_length=24, null=True),
            preserve_default=True,
        ),
    ]
