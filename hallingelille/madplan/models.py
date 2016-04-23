#This files using the following encoding:utf-8 
from django.db.models import *
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator

from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
# Create your models here.

from datetime import date, time, datetime, timedelta

from decimal import Decimal

import itertools

import cgi, urllib

TILMELDINGSFRIST_DAGE = settings.TILMELDINGSFRIST_DAGE or 3
MENUFRIST_DAGE = settings.MENUFRIST_DAGE or 7
FRISTER_TIL = settings.FRISTER_TIL or False
MAX_PRIS = 35
NY_PRIS_DATO=date(2016,4,5)


from util import *

def kommaliste(liste):
	liste = [unicode (x) for x in liste]
	l = len(liste)
	if l == 0: return ''
	if l == 1: return liste[0]
	return u' og '.join([u', '.join(liste[0:-1]),liste[-1]])

def remove_dups(seq):
    """Returns the elements of seq in the same order, with all duplicates removed"""
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

class Familie (Model):
	"""En familie er en gruppe personer der bor sammen og betaler sammen"""
	def __unicode__(self):
		return  self.medlemsliste()  + ' ('+  self.husstand.adresse + ')'
	husstand = ForeignKey('Husstand', on_delete=PROTECT)

	def medlemsliste(self):
		return kommaliste (self.person_set.all().order_by('foedselsdag'))

	class Meta:
		verbose_name_plural = 'Familier'
		ordering = ['husstand__adresse','id']

	def split(self):
		for p in self.person_set.all():
			f = Familie(husstand = self.husstand)
			f.save()
			p.familie = f
			p.save()
		self.delete()

class Husstand(Model):
	"""En Husstand er en eller flere familier, der bor på samme adresse"""
	def __unicode__(self):
		return self.adresse

	adresse = CharField(max_length = 40, unique=True)

	class Meta:
		verbose_name_plural = 'Husstande'
		ordering = ['adresse']



class Person(Model):
	def __unicode__(self):
		return self.navn

	navn = CharField(max_length = 60, unique=True)
	fornavn = CharField(max_length = 60,blank=True,null=True)
	efternavn = CharField(max_length = 60, blank=True,null=True)
	user = OneToOneField(User, blank=True,null=True,on_delete=SET_NULL)
	telefon = CharField(max_length=20, blank=True)
	foedselsdag = DateField(blank=True,null=True, verbose_name=u'fødselsdag')
	vis_foedselsdag = BooleanField(default=True)
	#husstand = ForeignKey(Husstand, blank=True, null=True, on_delete=SET_NULL)
	familie = ForeignKey(Familie,blank=True,null=True,on_delete=SET_NULL)
	#administrer_familie = BooleanField(default=False)
	er_beboer = BooleanField(default=True)

	def rfc_adresse(self):
		if self.user is None:
			return None
		else:
			return '"%s" <%s>' % (self.navn, self.user.email)
		

	def kan_administrere(self):
		return Person.objects.filter(familie__person=self)

	def alder(self,dato=None):
		if dato == None:
			dato = date.today()
		if self.foedselsdag:
			alder = dato.year-self.foedselsdag.year
			if dato < self.foedselsdag.replace(year=dato.year):
				alder = alder - 1
			return alder
		return None
			

	def prisgruppe(self,dato=None):
		if dato == None: dato = date.today()
		alder = self.alder(dato)
		if alder:
			if  alder < 4:
				return "Lille barn"
			if  alder < 12:
				return "Barn"

		periode = self.periodeperson_set.filter(periode__slutdato__gte=dato).order_by('periode__startdato').first()
		if dato < NY_PRIS_DATO:
			if periode:
				if periode.deltagelsesprocent == 0:
					return u"Gæst"

		if alder:
			if alder < 18:
				return "Teenager" #Teenagere er aldrig gæster
		return "Voksen"
	

	class Meta:
		verbose_name_plural = "Personer"
		ordering = ['navn']

class Madpraeferencer(Model):

	person = OneToOneField(Person, related_name="madpraeferencer")
	fritekst = TextField(blank=True,null=True, verbose_name="Præferencer") 
	minus_koed = BooleanField(verbose_name="Minus kød", default=False)
	minus_fisk = BooleanField(default=False)
	minus_gluten = BooleanField(default=False)
	minus_maelk = BooleanField(verbose_name="Minus mælk", default=False)



	class Meta:
		verbose_name_plural = "Madpræferencer"
		ordering = ["person__navn",]

class Periode(Model):
	def __unicode__(self):
		return str(self.startdato) + ' - ' + str(self.slutdato)

	startdato = DateField()
	slutdato = DateField()
	class Meta:
		verbose_name_plural = "Perioder"

	def clean(self, *args, **kwargs):
		pk = self.pk or -1
		if self.slutdato != None and self.startdato != None:
			if self.slutdato < self.startdato:
				raise ValidationError(u'Slutdato før startdato')
			if Periode.objects.filter(startdato__lte=self.slutdato, slutdato__gte=self.startdato).exclude(pk=pk).exists():
				raise ValidationError(u'Overlappende perioder')
	        super(Periode, self).clean(*args, **kwargs)

	def save(self, *args, **kwargs):
		ny = (self.pk == None)
		super(Periode,self).save(*args,**kwargs)
		if ny:
			self.kopier_forrige_deltagere()
			self.generer_maddage()

	def kopier_forrige_deltagere(self):
		""" Fejler hvis der ikke findes tidligere perioder"""
		try:		
			forrige_periode = Periode.objects.filter(slutdato__lt=self.startdato).order_by('-slutdato')[0]
			for pp in forrige_periode.periodeperson_set.all():
				PeriodePerson.objects.get_or_create(periode=self, person=pp.person, deltagelsesprocent = pp.deltagelsesprocent) 
		except:
			pass
			

	def generer_maddage(self):
		for d in range(0,(self.slutdato - self.startdato).days):
			dato = self.startdato + timedelta(days=d)
			if dato.isoweekday() in [1,7]:
				Maddag.objects.get_or_create(dato=dato, periode=self)


	def antal_maddage(self):
		return   Maddag.objects.filter(dato__range= (self.startdato,self.slutdato)).count()

class PeriodePerson(Model):
	def __unicode__(self):
		return self.person.navn

	person = ForeignKey(Person)
	periode = ForeignKey(Periode)
        deltagelsesprocent = IntegerField(default=0,choices=((a,str(a)+"%") for a in  (0,25,50,75,100)) )


	def save(self, *args, **kwargs):
	        super(PeriodePerson, self).save(*args, **kwargs)
		pers = self.person
		peri = self.periode
		tilmeldt = self.deltagelsesprocent > 0  
		for m in peri.maddag_set.all():
			t = Tilmelding.objects.get_or_create(maddag=m, person = pers, defaults={'tilmeldt': tilmeldt})


	class Meta:
		verbose_name = "Person i periode"
		verbose_name_plural = "Personer i periode"
		ordering = ['person__navn']
		unique_together = ('person','periode')

class Madhold(Model):
	def __unicode__(self):
		return self.navn + ': ' +  self.medlemsliste()

	navn = CharField(max_length = 60)
	medlemmer = ManyToManyField('Person', related_name="madhold", blank=True, null=True, db_table='madplan_person_hele_madhold')

	def mailto_link(self):
		
		adresser = [p.rfc_adresse() for p in self.medlemmer.all().select_related("user") if p.user is not None]
		
		result =  '<a href="mailto:%s">@</a>' %  (urllib.quote(u",".join(adresser).encode('utf8')))
		return result	

	mailto_link.allow_tags = True

	def medlemsliste(self):
		if self.medlemmer.exists():
			return   kommaliste(self.medlemmer.all())
		else:
			return "Tomt madhold"
		
	medlemsliste.allow_tags = True

	class Meta:
		ordering = ['navn']
		verbose_name_plural = 'Madhold'

def weekdaystring(d):
	return [u'søndag',u'mandag',u'tirsdag',u'onsdag',u'torsdag',u'fredag',u'lørdag',u'søndag'][d.isoweekday()] 

class Udlaeg(Model):
	maddag = ForeignKey('Maddag')
	person = ForeignKey(Person)
	beloeb = DecimalField(verbose_name=u'beløb', max_digits=6, decimal_places=2)
	afregnet = BooleanField(default=False)

	class Meta:
		verbose_name = u'Udlæg'		
		verbose_name_plural = u'Udlæg'		


def tilmeldingsfrist_fra_dato(dato):
	if dato.isoweekday == 1:
		return datetime.combine(dato - timedelta(days=3), time(0,0,1))
	if dato.isoweekday == 7:
		return datetime.combine(dato - timedelta(days=2), time(0,0,1))
	return datetime.combine(dato - timedelta(days=2), time(0,0,1))

class Maddag(Model):
	def __unicode__(self):
		#return self.dato.isoformat() # u'{0:%A} {0.day}. {0:%B}'.format(self.dato)
		if self.dato.year == date.today().year:
			return weekdaystring(self.dato) + ' ' +  u'{0.day}. {0:%B}'.format(self.dato)
		else:
			return weekdaystring(self.dato) + ' ' +  u'{0.day}. {0:%B} {0:%Y}'.format(self.dato)
	dato = DateField(primary_key=True)
	menu = TextField(max_length=4000, blank=True)
	menupris = DecimalField(verbose_name=u'beløb', max_digits=6, decimal_places=0, blank = True, null = True, validators=[MaxValueValidator(35)])
	madhold = OneToOneField(Madhold, blank=True, null=True)
	# This is not being stored, but copied in save()
	kopier_madhold_fra = ForeignKey(Madhold, blank=True, null=True, related_name='dummy') 
	periode = ForeignKey(Periode, blank=True)
	medspisere = ManyToManyField(Person, through='Tilmelding')
	alle_udlaeg_registreret = BooleanField(default=False, verbose_name="alle udlæg registreret")
	tillad_sen_tilmelding = BooleanField(default=False, verbose_name='Åben for sen tilmelding')

	def spisetid (self,naive=True):
		if naive:
			return datetime.combine(self.dato, time(18,0))
		else:
			return datetime.combine(self.dato, time(18,0,tzinfo=settings.LOCALTZ))
				

	def udlaeg_sum(self):
		return self.udlaeg_set.aggregate(total=Sum('beloeb'))['total'] or 0

	def detaljer (self):
		return 'Se/ret detaljer'

	def vis_menu (self):
		if self.menupris:
			prislinje = 'Pris: ' + str(self.menupris) + ':<br />'
		else:
			prislinje = ''
		vis_menu = prislinje + self.menu

		if not self.can_change_menu() and vis_menu == '' and self.madhold:
			vis_menu = u'<b>Madholdet -  %s - har ikke lagt en menu op. Sådan nogen slubberter!</b>' % self.madhold.medlemsliste()
		return mark_safe(vis_menu)

	def madhold_link(self):
		if self.madhold:
			return format_html(
				u'<a href="/admin/madplan/madhold/{0}">{1}</a>',
				self.madhold.pk,
				self.madhold.medlemsliste() 
			)
		else:
			return u''
	madhold_link.allow_tags = True
	madhold_link.short_description = 'Madhold' 
	
	def tilmeldte(self):
		return self.tilmelding_set.filter(tilmeldt=True)

	def antal_tilmeldte(self):
		return (self.tilmeldte().count() or 0) + (self.tilmelding_set.aggregate(Sum('gaester_voksne'))['gaester_voksne__sum'] or 0) + (self.tilmelding_set.aggregate(Sum('gaester_boern'))['gaester_boern__sum'] or 0)
		return 0

	def tilmeldte_tekst(self):
		ts = self.tilmeldte().order_by('person__familie__husstand','person__familie','person__foedselsdag')
		return  ", ".join(t.tilmeldte_tekst() for t in ts)
	tilmeldte_tekst.short_description = "Liste over tilmeldte"

	def tilmeldte_grupper(self):
		result = {}
		for t in self.tilmeldte():
			pg = t.person.prisgruppe(self.dato)
			if pg in (u'Gæst'):
				pg = 'Voksen'
			if pg in result.keys(): 
				result[pg] += 1
			else:
				result[pg] = 1

		gaester = self.tilmeldte().aggregate(Voksen=Sum('gaester_voksne'),Barn=Sum('gaester_boern'))
		for pg, value  in gaester.items():
			if value > 0:
				if pg in result.keys(): 
					result[pg] += value
				else:
					result[pg] = value


		result_str = ""
		for pg in ['Voksen','Teenager', 'Barn','Lille barn',u'Gæst']:
			if pg in result.keys():
				result_str += "%s: %s<br>" % (pg, result[pg])
		result_str += "<br>Budget: %s</br>" % (self.budget())
		result_str += "<br>" + self.madvanelink()

		return '<div style="white-space: nowrap">'+ result_str + '</div>'
	tilmeldte_grupper.allow_tags = True
	tilmeldte_grupper.short_description = "Tilmeldte"
	

	def budget(self):
		ts = self.tilmeldte() 
		return sum([t.pris_aktuel() for t in ts])

	def _save(self, *args,**kwargs):
		try:
			p = self.periode
		except:
			p = None
		if p == None:
			try:
				self.periode = Periode.objects.get(startdato__lte = self.dato, slutdato__gte = self.dato)
			except Periode.DoesNotExist:
				self.periode = None
				raise

		super(Maddag, self).save(*args, **kwargs)

		self.tilfoej_hvis_mangler() 

	def tilfoej_tilmeldinger(self):
		ts = []
		for pp in self.periode.periodeperson_set.all().exclude(person__tilmelding__maddag=self):
			tilmeldt = pp.deltagelsesprocent > 0
			t = Tilmelding(maddag=self, person = pp.person, tilmeldt=tilmeldt)
			ts.append(t)
		Tilmelding.objects.bulk_create(ts)

	def tilfoej_hvis_mangler(self):
		if self.periode.periodeperson_set.count() > self.tilmelding_set.count():
			self.tilfoej_tilmeldinger()
			
	def tilfoej_alle_tilmeldinger(self):
		for m in Maddag.objects.all():
			m.tilfoej_hvis_mangler()
				
	def genskab_tilmeldinger(self):
		self.tilmelding_set.all().delete()
		self.tilfoej_tilmeldinger()

	def save(self, *args, **kwargs):
		if not self.can_change_menu():
			try:
				old = Maddag.objects.get(pk=self.pk)
				if old.menupris > 0 and self.menupris > old.menupris:
					raise PermissionDenied("Kan ikke øge prisen")
			except Maddag.DoesNotExist:
				pass

		if self.madhold == None:
			self.madhold = Madhold.objects.create(navn=self.dato.strftime('%Y-%m-%d'))
		kopi = self.kopier_madhold_fra
		self.kopier_madhold_fra = None
		if kopi != None:
			self.madhold.medlemmer = kopi.medlemmer.all()
			self.madhold.save()
		self._save(*args,**kwargs)
		
	def can_change_menu(self):
		if (self.dato - date.today()).days < MENUFRIST_DAGE and FRISTER_TIL:
			return False
		else:
			return True

	def madvanelink(self):
		return '<a href="/madvaner/%s">Madvaner</a>' % (self.dato)
	madvanelink.allow_tags = True

	class Meta:
		verbose_name_plural = "Maddage"
		#ordering = [ 'dato']

class Tilmelding(Model):
	person = ForeignKey(Person)
	maddag = ForeignKey(Maddag)
	tilmeldt = BooleanField(default=False)
	gaester_voksne = IntegerField(u'Gæster voksne',default=0)
	gaester_boern = IntegerField(u'Gæster børn',default=0)

	afregnet = BooleanField(default=False)

	def pris(self,ag=None):
		if ag == None:
			ag = self.person.prisgruppe(self.maddag.dato)
		menupris = self.maddag.menupris 
		
                if menupris == None:
                        if self.maddag.dato > date(2015,6,3):
                                menupris = Decimal(25)
                        	if self.maddag.dato < date.today() + timedelta(days=7):
        	                      	self.maddag.menupris = menupris
	        	                self.maddag.save()
                        else:
				return 0


		if ag == 'Lille barn':
			return 0
		if ag == 'Barn':
			return menupris/2
		if ag == 'Teenager':
			return menupris
		if ag == 'Voksen':
			return menupris
		if ag == u'Gæst':
			if self.maddag.dato < NY_PRIS_DATO:
				return menupris + 20
			else: 
				return menupris

		raise 'Ugyldig Aldersgruppe: ' + ag  


	def pris_aktuel(self):
		return (self.pris()  if self.tilmeldt else 0) + self.gaester_voksne * self.pris(u'Gæst')   + self.gaester_boern * self.pris('Barn')

	def tilmeldt_fra_familie(self):
		return ", ".join(t.tilmeldte_tekst() for t in self.maddag.tilmeldte().filter(person__familie__person=self.person))

	def tilmeldte_tekst(self):
		result = ''
		if self.tilmeldt:
			result += self.person.navn
		gaester = self.gaester_voksne + self.gaester_boern
		if gaester > 1:
			result += u' + %s gæster' % gaester
		if gaester == 1:
			result += u' + 1 gæst'
		return result			
			

	class Meta:
		verbose_name_plural = "Tilmeldinger"
		#ordering = ['person__familie__husstand','person__familie','person','maddag']
		unique_together = ('person','maddag')

	def operation(new,old):
		'Den mest omfattende operation - afmeld > tilmeld > opret > ingen'
		if old == None:
			return 'Opret'
		if old.pris_aktuel() == new.pris_aktuel():
			return 'Ingen'
		if old.pris_aktuel() > new.pris_aktuel():
			return 'Afmeld'
		return 'Tilmeld'

	def can_change(self):
		return 'Tilmeld' in self.tilladte_aendringer()

	def aaben(self):
		if self.can_change():
			return mark_safe( u'<img src="/static/admin/img/icon-yes.gif" alt="Åben" title="Åben"" />')
		else:
			return mark_safe(u'<img src="/static/admin/img/icon-no.gif" alt="Lukket" title="Lukket"" />')

	aaben.short_description = u'Åben'
	


	def tilladte_aendringer(self,nu=None):
		if nu == None: 
			nu = datetime.now()
		result = set(['Ingen', 'Opret'])
		m = self.maddag
		d = m.dato
		if ((not FRISTER_TIL) or 
		    (self.maddag.tillad_sen_tilmelding and nu < self.maddag.spisetid()) or 
		    nu < tilmeldingsfrist_fra_dato(d)
		):
			result.update(['Afmeld','Tilmeld'])

		if nu > self.maddag.spisetid() and not self.afregnet:
			result.update(['Tilmeld'])
		return result
		
	def save(self, *args,**kwargs):
		try:
			old = Tilmelding.objects.get(pk=self.pk)
		except Tilmelding.DoesNotExist:
			old = None
		operation = self.operation(old)
		if not operation in self.tilladte_aendringer(datetime.now()):
			raise PermissionDenied(u'Kan ikke til-/afmelde på nuværende tidspunkt')
		super(Tilmelding,self).save(*args,**kwargs)


class AdmMadhold(Madhold):
	class Meta:
		proxy = True
		verbose_name = 'Madhold (Admin)'
		verbose_name_plural = 'Madhold (Admin)'

class AdmMaddag(Maddag):
	class Meta:
		proxy = True
		verbose_name = 'Maddag (Admin)'
		verbose_name_plural = 'Maddage (Admin)'

	def can_change_menu(self):
		return True

class AdmTilmelding(Tilmelding):
	class Meta:
		proxy = True
		verbose_name = 'Tilmelding (Admin)'
		verbose_name_plural = 'Tilmeldinger (Admin)'

	def can_change(self):
		return True


	def tilladte_aendringer(self,nu=None):
		result = set(['Opret','Afmeld','Tilmeld', 'Ingen'])
		return result
