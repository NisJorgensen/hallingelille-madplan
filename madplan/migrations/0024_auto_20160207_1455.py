# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0023_remove_person_madpraeferencer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madpraeferencer',
            name='person',
            field=models.OneToOneField(related_name='madpraeferencer', to='madplan.Person'),
            preserve_default=True,
        ),
    ]
