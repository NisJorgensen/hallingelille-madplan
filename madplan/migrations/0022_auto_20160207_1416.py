# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.db import models, migrations

def flyt_praeferencer(apps, schema_editor):
	Person = apps.get_model("madplan", "Person")
	Madpraef = apps.get_model("madplan", "Madpraeferencer")
	for person in Person.objects.all():
		m = Madpraef(person=person)
		tekst = person.madpraeferencer
		if tekst:
			m.fritekst = tekst
			if re.search("Vegetar",tekst, flags=re.I):
				m.minus_koed=True
				if not re.search("spiser (\w* )?fisk",tekst,flags=re.I):
					m.minus_fisk = True
			if re.search("gluten", tekst,flags=re.I):
				m.minus_gluten = True
			if re.search("mælk", tekst,flags=re.I):
				m.minus_maelk = True
		m.save()


def flyt_praeferencer_tilbage(apps, schema_editor):
	Madpraef = apps.get_model("madplan", "Madpraeferencer")
	Madpraef.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('madplan', '0021_madpraeferencer'),
    ]

    operations = [
	migrations.RunPython(flyt_praeferencer,flyt_praeferencer_tilbage),

    ]
