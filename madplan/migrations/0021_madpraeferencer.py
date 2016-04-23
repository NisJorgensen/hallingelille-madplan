# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0020_auto_20151213_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Madpraeferencer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fritekst', models.TextField(null=True, verbose_name=b'Pr\xc3\xa6ferencer', blank=True)),
                ('minus_koed', models.BooleanField(default=False, verbose_name=b'Minus k\xc3\xb8d')),
                ('minus_fisk', models.BooleanField(default=False)),
                ('minus_gluten', models.BooleanField(default=False)),
                ('minus_maelk', models.BooleanField(default=False, verbose_name=b'Minus m\xc3\xa6lk')),
                ('person', models.OneToOneField(related_name='praeferencer', to='madplan.Person')),
            ],
            options={
                'verbose_name_plural': 'Madpr\xe6ferencer',
            },
            bases=(models.Model,),
        ),
    ]
