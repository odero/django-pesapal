# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pesapal_transaction', uuidfield.fields.UUIDField(max_length=32)),
                ('merchant_reference', models.IntegerField(db_index=True)),
                ('amount', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='transaction',
            unique_together=set([('merchant_reference', 'pesapal_transaction')]),
        ),
    ]
