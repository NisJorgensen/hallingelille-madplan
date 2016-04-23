# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0003_auto_20141228_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madhold',
            name='medlemmer',
            field=models.ManyToManyField(related_name=b'madhold', null=True, to=b'madplan.Person', db_table=b'madplan_person_hele_madhold', blank=True),
        ),
    ]
