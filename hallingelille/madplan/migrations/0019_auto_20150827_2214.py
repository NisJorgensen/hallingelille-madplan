# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0018_auto_20150616_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='madpraeferencer',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='foedselsdag',
            field=models.DateField(null=True, verbose_name='f\xf8dselsdag', blank=True),
            preserve_default=True,
        ),
    ]
