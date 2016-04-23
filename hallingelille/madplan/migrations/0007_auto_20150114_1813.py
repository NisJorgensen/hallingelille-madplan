# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0006_auto_20150114_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maddag',
            name='menupris',
            field=models.DecimalField(null=True, verbose_name='bel\xf8b', max_digits=6, decimal_places=0, blank=True),
        ),
    ]
