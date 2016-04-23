# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0009_auto_20150115_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maddag',
            name='madhold',
            field=models.OneToOneField(null=True, blank=True, to='madplan.Madhold'),
        ),
    ]
