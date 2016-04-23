# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0019_auto_20150827_2214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='maddag',
            options={'verbose_name_plural': 'Maddage'},
        ),
        migrations.AddField(
            model_name='person',
            name='efternavn',
            field=models.CharField(max_length=60, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='fornavn',
            field=models.CharField(max_length=60, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='vis_foedselsdag',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
