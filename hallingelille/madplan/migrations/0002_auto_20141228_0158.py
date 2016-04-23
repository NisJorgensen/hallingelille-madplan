# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AfregningsPeriode',
        ),
        migrations.DeleteModel(
            name='AdmHusstand',
        ),
        migrations.DeleteModel(
            name='AdmMaddag',
        ),
        migrations.DeleteModel(
            name='AdmMadhold',
        ),
        migrations.DeleteModel(
            name='AdmPeriodePerson',
        ),
        migrations.DeleteModel(
            name='AdmPerson',
        ),
        migrations.DeleteModel(
            name='AdmTilmelding',
        ),
        migrations.AlterModelOptions(
            name='familie',
            options={'ordering': ['husstand__adresse'], 'verbose_name_plural': 'Familier'},
        ),
        migrations.RemoveField(
            model_name='maddag',
            name='aktueltmadhold',
        ),
        migrations.RemoveField(
            model_name='maddag',
            name='oprindeligtmadhold',
        ),
        migrations.DeleteModel(
            name='KonkretMadhold',
        ),
        migrations.RemoveField(
            model_name='madhold',
            name='budgetansvarlig',
        ),
        migrations.AlterField(
            model_name='maddag',
            name='madhold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.Madhold', null=True),
        ),
        migrations.DeleteModel(
            name='FastMadhold',
        ),
    ]
