# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0014_auto_20150118_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdmMaddag',
            fields=[
            ],
            options={
                'verbose_name': 'Maddag (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Maddage (Admin)',
            },
            bases=('madplan.maddag',),
        ),
        migrations.CreateModel(
            name='AdmMadhold',
            fields=[
            ],
            options={
                'verbose_name': 'Madhold (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Madhold (Admin)',
            },
            bases=('madplan.madhold',),
        ),
        migrations.CreateModel(
            name='AdmTilmelding',
            fields=[
            ],
            options={
                'verbose_name': 'Tilmelding (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Tilmeldinger (Admin)',
            },
            bases=('madplan.tilmelding',),
        ),
    ]
