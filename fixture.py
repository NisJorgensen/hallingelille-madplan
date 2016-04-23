#!/usr/bin/python
# coding: utf-8
from madplan.models import *
from django.contrib.auth.models import User

import datetime

pp = Periode(startdato="2013-08-11",slutdato="2013-12-12")
pp.save()
pp = Periode.objects.all()[0]
st = pp.startdato
while st < pp.slutdato:
	if st.isoweekday() in [1,3,4,7]:
		Maddag(dato=st, periode=pp).save()
	st = st + datetime.timedelta(days=1)

for n in """Charlotte,71
Sten,71
Mia J,71
Lasse,71
Bettina,71
Camilla N-E,71
Nis,71
Louise S-T,71
Anne,2
Søren,2
Jørgen,4
Lisbet,4
Steen,4
Mads,4
Ulla,4
Rita,4
Jesper L,6
Mette,6
Chris,8
Anne-Mette,8
Kim,8
Sekita,8
Else,10
Esben,14
Lotta,14
Bjørn,16
Sasja,16
Susanna,18
Line,18
John,20
Katrine,20
Annette B H,22
Nikolaj Holt,22
Annette C H,24
Michael,24
Sofia,26
Prokop,26
Bettii,26
Lars G,26
Elin, 28
Benedikte,28
Mia L,13
Nikolaj Hem,9
Louise H,9
Lars B,7
Melissa,7
Jonas,5
Camilla B,5
Jesper J,3
Gitte,3""".split("\n"):
	(navn,adresse) = n.split(",")
	if adresse == 71:
		adresse = "Valsømaglevej 71"
	else:
		adresse = "Hallingebjergvej %s" % adresse
	u,_ = User.objects.get_or_create(username=navn.replace(" ",""))
	u.set_password('foobar')
	u.save()
		
	h,_ = Husstand.objects.get_or_create(adresse=adresse)
	p,_ = Person.objects.get_or_create(navn=navn, user=u, husstand=h)
	PeriodePerson.objects.get_or_create(periode = pp, person =p)

