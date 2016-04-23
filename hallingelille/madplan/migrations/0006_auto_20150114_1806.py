# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0005_periodeperson_deltagelsesprocent'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='menupris',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='menupris',
            name='menutype',
        ),
        migrations.DeleteModel(
            name='Menupris',
        ),
        migrations.RemoveField(
            model_name='maddag',
            name='menutype',
        ),
        migrations.DeleteModel(
            name='Menutype',
        ),
        migrations.AddField(
            model_name='maddag',
            name='menupris',
            field=models.DecimalField(default=30, verbose_name='bel\xf8b', max_digits=6, decimal_places=0),
            preserve_default=False,
        ),
    ]
