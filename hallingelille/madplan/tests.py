#This files using the following encoding:utf-8 
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import *
from datetime import datetime, time, date, timedelta

class BaseTestCase(TestCase):
	def setUp(self):
		h = Husstand.objects.create(adresse='Vimmersvej')
		f = Familie.objects.create(husstand=h)
		p = Person.objects.create(navn="Test", familie=f)
		p2 = Person.objects.create(navn="Test 2", familie=f)
		p3 = Person.objects.create(navn="Test 3" )
		peri = Periode.objects.create(startdato=date.today()+timedelta(days=-20),slutdato=date.today()+timedelta(days=20) )
		pp = PeriodePerson.objects.create(periode = peri,person = p, deltagelsesprocent = 50)
		pp = PeriodePerson.objects.create(periode = peri,person = p2, deltagelsesprocent = 50)
		pp = PeriodePerson.objects.create(periode = peri,person = p3, deltagelsesprocent = 0)


class TilmeldingGaesterTestCase(BaseTestCase):
	
	def test_periode_person(self):
		self.assertEqual(Husstand.objects.count(),1)
		m = Maddag.objects.all()[0]
		m.tilmelding_set.update(tilmeldt=False)
		self.assertEqual(Tilmelding.objects.filter(maddag=m).count(),3)
		self.assertEqual(m.antal_tilmeldte(),0)
		t = m.tilmelding_set.get(person__navn='Test')
		t.tilmeldt = True
		t.save()
		self.assertEqual(m.antal_tilmeldte(),1)
		self.assertEqual(m.tilmeldte_tekst(),'Test')
		t.gaester_voksne = 1
		t.gaester_boern = 2
		t.save()
		self.assertEqual(m.antal_tilmeldte(),4)
		self.assertEqual(m.tilmeldte_tekst(),u'Test + 3 gæster')
		#self.assertEqual(m.tilmeldte_tekst(),'Test + 3 gæster (2 voksne, 1 barn)')
		self.assertEqual(m.tilmeldte_grupper(),'Voksen: 2<br>Barn: 2<br>')
		self.assertEqual(m.budget(),95)
		

class TilmeldingsfristTestCase(BaseTestCase):
	def test_tilmeldings_frist(self):
		d = date.today()
		m,_ = Maddag.objects.get_or_create(dato=d-timedelta(days=1))
		p = Person.objects.all()[0]
		t = Tilmelding.objects.get(person=p,maddag=m)
		self.assertEqual(t.can_change(),True)
		t.tilmeldt = True
		t.save()
		t = Tilmelding.objects.get(maddag=m, person=p)
		self.assertEqual(t.tilmeldt, True)
		#self.assertEqual(t.can_change(),False)
		t.tilmeldt = False
		self.assertRaises(PermissionDenied, t.save)
		t = Tilmelding.objects.get(maddag=m,person=p)
		self.assertEqual(t.tilmeldt, True)


	def test_tilladte_aendringer(self):
		self.assertEqual(settings.FRISTER_TIL, True)
		d = date.today() + timedelta(days=4)
		foer_spisetid = datetime.combine(d, time(17,45)) 
		efter_spisetid = datetime.combine(d, time(18,15)) 
		tre_dage_foer = datetime.combine(d,time()) - timedelta(days=3 )
		to_dage_foer = datetime.combine(d,time()) - timedelta(days=2)
		en_dage_foer = datetime.combine(d,time()) - timedelta(days=1)
		p = Person.objects.all()[0]
		m,_ = Maddag.objects.get_or_create(dato=d)
		m.tillad_sen_tilmelding = False
		m.save()
		t = Tilmelding.objects.get(maddag=m, person=p)
		t.nu = tre_dage_foer
		self.assertEqual (t.tilladte_aendringer(tre_dage_foer), set(['Ingen', 'Opret', 'Tilmeld','Afmeld']))
		self.assertEqual (t.tilladte_aendringer(to_dage_foer), set(['Ingen', 'Opret']))
		self.assertEqual (t.tilladte_aendringer(foer_spisetid), set(['Ingen', 'Opret']))
		self.assertEqual (t.tilladte_aendringer(efter_spisetid), set(['Ingen', 'Opret','Tilmeld']),"%s %s" % (t.maddag.spisetid(), efter_spisetid ))
		m.tillad_sen_tilmelding = True
		m.save()
		t = Tilmelding.objects.get(maddag=m, person=p)
		self.assertEqual (t.tilladte_aendringer(foer_spisetid), set(['Ingen', 'Opret', 'Afmeld', 'Tilmeld']))
		self.assertEqual (t.tilladte_aendringer(to_dage_foer), set(['Ingen', 'Opret', 'Afmeld', 'Tilmeld']))
		self.assertEqual (t.tilladte_aendringer(efter_spisetid), set(['Ingen', 'Opret','Tilmeld']))

class AdministrerTestCase(BaseTestCase):
	def test_kan_administrere(self):
		p = Person.objects.get(navn='Test')
		self.assertEqual(set(p.kan_administrere()),set([Person.objects.get(navn='Test 2'),p]))
