# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20170906_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='private',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='api_requests_count',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
