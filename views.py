#!/usr/bin/python
#coding: utf-8
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django import http
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth import SESSION_KEY
from  django.http import HttpResponse, HttpResponseNotFound
import unicodecsv as csv
from hallingelille.madplan.models import *


@user_passes_test(lambda u: u.is_superuser)
def become(request, user, redirect_url='/'):
    su_user = get_object_or_404(User, username=user, is_active=True)
    request.session[SESSION_KEY] = su_user.id
    return http.HttpResponseRedirect(redirect_url)

		
def boerneliste(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="boerneliste.csv"'
	writer = csv.writer(response, delimiter=";")
	#qs = Person.objects.all().filter(foedselsdag__gte=date.today()-timedelta(days=21*366))
	qs = Person.objects.all().order_by("familie__husstand__adresse")
	writer.writerow(["Navn","Husstand","Foedselsdag","Alder i dag"])
	for p in qs:
		writer.writerow([p.navn,p.familie.husstand, p.foedselsdag,p.alder(date.today())])
	return response
