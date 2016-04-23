# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0017_auto_20150616_1104'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='familie',
            options={'ordering': ['husstand__adresse', 'id'], 'verbose_name_plural': 'Familier'},
        ),
    ]
