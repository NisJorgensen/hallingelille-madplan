#!/usr/bin/python
#coding: utf-8

# Create your views here.

from datetime import date, datetime, time, timedelta

from django.contrib.auth.decorators import login_required, permission_required
from  django.http import HttpResponse, HttpResponseNotFound
import csv
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import django
from django.forms import widgets
from .models import *

def index(request):
	 return redirect("/admin")
	
class PeriodeForm(django.forms.Form):
	startdato=django.forms.DateField()
	slutdato=django.forms.DateField()

class AfregnetForm(django.forms.Form):
	startdato=django.forms.DateField(widget=widgets.HiddenInput)
	slutdato=django.forms.DateField(widget=widgets.HiddenInput)

def qsa(startdato, slutdato):
	return Tilmelding.objects.filter(
		Q(maddag__dato__range=(startdato,slutdato)), 
		Q(afregnet=False),
	).order_by(
		'person__familie__husstand__adresse',
		'person__familie__id',
		'maddag__dato',
		'person__foedselsdag',
		'person__navn'
	).select_related('person','maddag', 'person__familie', 'person__familie__husstand')
	
def periodestart():
	try:
		start = qsa('2013-01-01','2099-12-31').order_by('maddag__dato')[0].maddag.dato
	except:
		start = date.today()
	return start
		
def periodeslut():
	return date.today() + timedelta(days=TILMELDINGSFRIST_DAGE-1)

@permission_required('madplan.admtilmelding_change')
def afregning(request):
	if request.method == 'GET':
		inddata = PeriodeForm(request.GET)
		inddata.is_valid()
		startdato=inddata.cleaned_data.get('startdato') or periodestart() 
		slutdato=inddata.cleaned_data.get('slutdato') or periodeslut()
		periodeform = PeriodeForm(initial={'startdato':startdato,'slutdato':slutdato})
		periodeform.is_valid()
		afregnetform = AfregnetForm(initial={'startdato':startdato,'slutdato':slutdato})
		qs = qsa(startdato,slutdato)
		context = {'queryset':qs, 'startdato' : startdato, 'slutdato': slutdato , 'periodeform' : periodeform, 'afregnetform': afregnetform}
		return render(request,'afregning.html', context)

	if request.method == 'POST':
		inddata = PeriodeForm(request.POST)
		if inddata.is_valid():
			startdato=inddata.cleaned_data.get('startdato') or periodestart() 
			slutdato=inddata.cleaned_data.get('slutdato') or periodeslut()
			qs = qsa(startdato,slutdato)
			qs.update(afregnet=True)
			return redirect('/afregning?%s' % qs.count())
		else:
			return redirect('/afregning')



def qsau(startdato, slutdato):
	return Udlaeg.objects.filter(
		maddag__dato__range=(startdato,slutdato), 
		afregnet=False
	).order_by(
		'maddag__dato'
	).select_related('person','maddag')

@permission_required('madplan.udlaeg_change')
def afregning_udlaeg(request):
	if request.method == 'GET':
		inddata = PeriodeForm(request.GET)
		inddata.is_valid()
		startdato=inddata.cleaned_data.get('startdato') or date(2013,8,1)
		slutdato=inddata.cleaned_data.get('slutdato') or  date.today()
		periodeform = PeriodeForm(initial={'startdato':startdato,'slutdato':slutdato})
		periodeform.is_valid()
		afregnetform = AfregnetForm(initial={'startdato':startdato,'slutdato':slutdato})
		qs = qsau(startdato,slutdato)
		context = {'queryset':qs, 'startdato' : startdato, 'slutdato': slutdato , 'periodeform' : periodeform, 'afregnetform': afregnetform}
		return render(request,'afregning_udlaeg.html', context)

	if request.method == 'POST':
		inddata = PeriodeForm(request.POST)
		if inddata.is_valid():
			startdato=inddata.cleaned_data.get('startdato') 
			slutdato=inddata.cleaned_data.get('slutdato') 
			qs = qsau(startdato,slutdato)
			qs.update(afregnet=True)
			return redirect('/afregning_udlaeg?%s' % qs.count())
		else:
			return redirect('/afregning_udlaeg')


def maddag(request, dato):
	dato = datetime.strptime(dato,'%Y-%m-%d')
	maddag = Maddag.objects.get(dato=dato)
	return render(request,'maddag.html', {'maddag': maddag})
	
	
#@permission_required('madplan.tilmelding_change')
def madvaner(request):
	periode = Periode.objects.get(startdato__lte=date.today(),slutdato__gte=date.today())
	qs1 = Person.objects.filter(madpraeferencer__fritekst__gt="", periodeperson__periode=periode, periodeperson__deltagelsesprocent__gt=0).order_by('familie', '-foedselsdag')
	qs2 = Person.objects.filter(madpraeferencer__fritekst__gt="", periodeperson__periode=periode, periodeperson__deltagelsesprocent=0).order_by('familie', '-foedselsdag')
	context = {'qs1': qs1, 'qs2': qs2}
	return render(request,'madvaner.html', context)

def madvaner_for_dato(request,dato):
	maddag = get_object_or_404(Maddag, dato=dato)
	qs = Person.objects.filter(madpraeferencer__fritekst__gt="", tilmelding__maddag = maddag, tilmelding__tilmeldt = True).order_by('familie', '-foedselsdag')

	context = {'qs': qs, 'title': "Personer tilmeldt %s" % (dato) }
	return render(request,'madvaner_dato.html', context)

