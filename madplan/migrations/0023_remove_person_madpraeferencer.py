# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0022_auto_20160207_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='madpraeferencer',
        ),
    ]
