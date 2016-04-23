# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0004_auto_20141228_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodeperson',
            name='deltagelsesprocent',
            field=models.IntegerField(default=0, choices=[(0, b'0%'), (25, b'25%'), (50, b'50%'), (75, b'75%'), (100, b'100%')]),
            preserve_default=True,
        ),
    ]
