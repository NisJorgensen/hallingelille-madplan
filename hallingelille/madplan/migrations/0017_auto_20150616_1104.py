# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0016_admmaddag_admmadhold_admtilmelding'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='er_beboer',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='familie',
            name='husstand',
            field=models.ForeignKey(to='madplan.Husstand', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='maddag',
            name='menupris',
            field=models.DecimalField(decimal_places=0, validators=[django.core.validators.MaxValueValidator(35)], max_digits=6, blank=True, null=True, verbose_name='bel\xf8b'),
            preserve_default=True,
        ),
    ]
