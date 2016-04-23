# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0011_auto_20150117_2343'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='periodeperson',
            unique_together=set([('person', 'periode')]),
        ),
    ]
