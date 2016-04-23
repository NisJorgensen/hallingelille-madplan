# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0008_auto_20150114_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='maddag',
            name='kopier_madhold_fra',
            field=models.ForeignKey(related_name=b'dummy', blank=True, to='madplan.Madhold', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maddag',
            name='madhold',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.Madhold'),
        ),
    ]
