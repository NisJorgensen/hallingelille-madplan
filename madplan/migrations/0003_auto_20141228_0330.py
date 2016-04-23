# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0002_auto_20141228_0158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='madhold',
            old_name='hele_medlemmer',
            new_name='medlemmer',
        ),
        migrations.RemoveField(
            model_name='madhold',
            name='halve_medlemmer',
        ),
        migrations.RemoveField(
            model_name='periodeperson',
            name='deltagelsesprocent',
        ),
    ]
