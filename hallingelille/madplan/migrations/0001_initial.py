# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AfregningsPeriode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startdato', models.DateField()),
                ('slutdato', models.DateField()),
            ],
            options={
                'ordering': ['startdato'],
                'verbose_name': 'Afregningsperiode',
                'verbose_name_plural': 'Afregningsperioder',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Familie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Familier',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Husstand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('adresse', models.CharField(unique=True, max_length=40)),
            ],
            options={
                'ordering': ['adresse'],
                'verbose_name_plural': 'Husstande',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Maddag',
            fields=[
                ('dato', models.DateField(serialize=False, primary_key=True)),
                ('menu', models.TextField(max_length=4000, blank=True)),
                ('alle_udlaeg_registreret', models.BooleanField(default=False, verbose_name=b'alle udl\xc3\xa6g registreret')),
                ('tillad_sen_tilmelding', models.BooleanField(default=False, verbose_name=b'\xc3\x85ben for sen tilmelding')),
            ],
            options={
                'ordering': ['dato'],
                'verbose_name_plural': 'Maddage',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Madhold',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('navn', models.CharField(max_length=60)),
            ],
            options={
                'ordering': ['navn'],
                'verbose_name_plural': 'Madhold',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KonkretMadhold',
            fields=[
                ('madhold_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='madplan.Madhold')),
            ],
            options={
                'ordering': ['navn'],
                'verbose_name': 'Madhold',
                'verbose_name_plural': 'Madhold',
            },
            bases=('madplan.madhold',),
        ),
        migrations.CreateModel(
            name='FastMadhold',
            fields=[
                ('madhold_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='madplan.Madhold')),
            ],
            options={
                'verbose_name': 'Madhold',
                'verbose_name_plural': 'Madhold',
            },
            bases=('madplan.madhold',),
        ),
        migrations.CreateModel(
            name='Menupris',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prisgruppe', models.CharField(max_length=20, choices=[(b'Voksen', b'Voksen'), (b'Barn', b'Barn'), (b'Lille barn', b'Lille barn'), (b'G\xc3\xa6st', b'G\xc3\xa6st')])),
                ('pris', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'Menupriser',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menutype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('navn', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Menutyper',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startdato', models.DateField()),
                ('slutdato', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Perioder',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PeriodePerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deltagelsesprocent', models.IntegerField(default=0, choices=[(0, b'0%'), (25, b'25%'), (50, b'50%'), (75, b'75%'), (100, b'100%')])),
                ('periode', models.ForeignKey(to='madplan.Periode')),
            ],
            options={
                'ordering': ['person__navn'],
                'verbose_name': 'Person i periode',
                'verbose_name_plural': 'Personer i periode',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('navn', models.CharField(unique=True, max_length=60)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('telefon', models.CharField(max_length=20, blank=True)),
                ('foedselsdag', models.DateField(null=True, verbose_name='Foedselsdag', blank=True)),
                ('familie', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.Familie', null=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['navn'],
                'verbose_name_plural': 'Personer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tilmelding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tilmeldt', models.BooleanField(default=False)),
                ('gaester_voksne', models.IntegerField(default=0, verbose_name='G\xe6ster voksne')),
                ('gaester_boern', models.IntegerField(default=0, verbose_name='G\xe6ster b\xf8rn')),
                ('afregnet', models.BooleanField(default=False)),
                ('maddag', models.ForeignKey(to='madplan.Maddag')),
                ('person', models.ForeignKey(to='madplan.Person')),
            ],
            options={
                'ordering': ['person__familie__husstand', 'person__familie', 'person', 'maddag'],
                'verbose_name_plural': 'Tilmeldinger',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Udlaeg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beloeb', models.DecimalField(verbose_name='bel\xf8b', max_digits=6, decimal_places=2)),
                ('afregnet', models.BooleanField(default=False)),
                ('maddag', models.ForeignKey(to='madplan.Maddag')),
                ('person', models.ForeignKey(to='madplan.Person')),
            ],
            options={
                'verbose_name': 'Udl\xe6g',
                'verbose_name_plural': 'Udl\xe6g',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='tilmelding',
            unique_together=set([('person', 'maddag')]),
        ),
        migrations.AddField(
            model_name='periodeperson',
            name='person',
            field=models.ForeignKey(to='madplan.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menupris',
            name='menutype',
            field=models.ForeignKey(to='madplan.Menutype'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menupris',
            unique_together=set([('prisgruppe', 'menutype')]),
        ),
        migrations.AddField(
            model_name='madhold',
            name='budgetansvarlig',
            field=models.ForeignKey(related_name=b'+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='madhold',
            name='halve_medlemmer',
            field=models.ManyToManyField(related_name=b'halve_madhold', null=True, to='madplan.Person', db_table=b'madplan_person_halve_madhold', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='madhold',
            name='hele_medlemmer',
            field=models.ManyToManyField(related_name=b'hele_madhold', null=True, to='madplan.Person', db_table=b'madplan_person_hele_madhold', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='aktueltmadhold',
            field=models.ForeignKey(related_name=b'aktuelle_maddage', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'Aktuelt madhold', blank=True, to='madplan.KonkretMadhold', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='madhold',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.FastMadhold', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='medspisere',
            field=models.ManyToManyField(to='madplan.Person', through='madplan.Tilmelding'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='menutype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.Menutype', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='oprindeligtmadhold',
            field=models.ForeignKey(related_name=b'oprindelige_maddage', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='madplan.KonkretMadhold', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='maddag',
            name='periode',
            field=models.ForeignKey(blank=True, to='madplan.Periode', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='familie',
            name='husstand',
            field=models.ForeignKey(to='madplan.Husstand'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='AdmHusstand',
            fields=[
            ],
            options={
                'ordering': ['adresse'],
                'verbose_name': 'Husstand (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Husstande (Admin)',
            },
            bases=('madplan.husstand',),
        ),
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
            name='AdmPeriodePerson',
            fields=[
            ],
            options={
                'verbose_name': 'Person i periode (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Personer i periode (Admin)',
            },
            bases=('madplan.periodeperson',),
        ),
        migrations.CreateModel(
            name='AdmPerson',
            fields=[
            ],
            options={
                'verbose_name': 'Person (Admin)',
                'proxy': True,
                'verbose_name_plural': 'Personer (Admin)',
            },
            bases=('madplan.person',),
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
