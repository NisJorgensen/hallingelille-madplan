# encoding: utf-8
from django.contrib import admin
from hallingelille import madplan
from hallingelille.admincsv import export_as_csv
from models import *
import django.forms as forms
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin import SimpleListFilter

import django.conf.urls 

from datetime import datetime, date, time, timedelta
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import  get_object_or_404, redirect

class ActionInChangeFormMixin(object):
    def response_action(self, request, queryset):
        """
        Prefer http referer for redirect
        """
        response = super(ActionInChangeFormMixin, self).response_action(request,
                queryset)
        if isinstance(response, HttpResponseRedirect):
            response['Location'] = request.META.get('HTTP_REFERER', response.url)
        return response  

    def change_view(self, request, object_id, extra_context=None):
        actions = self.get_actions(request)
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = self.get_action_choices(request)
        else: 
            action_form = None
        return super(ActionInChangeFormMixin, self).change_view(request, object_id, extra_context={
            'action_form': action_form,
        })

def add_link_field(target_model = None, field = '', link_text = unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            app_name = instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
            url = reverse(reverse_path, args = (link_obj.id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name + ' link'
        cls.link = link
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + ['link']
        return cls
    return add_link

class CustomUserAdmin(UserAdmin):

	def reset_user_password(self, user):
            form = PasswordResetForm(data={'email': user.email})
            form.is_valid()
            form.save(email_template_name='registration/password_reset_email.html')

        def reset_password(self, request, user_id):
            if not self.has_change_permission(request):
                raise PermissionDenied
            user = get_object_or_404(self.model, pk=user_id)
            self.reset_user_password(user)    
            return redirect('..')

        def reset_passwords(self, request, queryset):
            for user in queryset:
            	self.reset_user_password(user)    

	actions = [reset_passwords,]

	list_display = ['username','email', 'is_staff', 'last_login']

        def get_urls(self):
            urls = super(CustomUserAdmin, self).get_urls()
            my_urls = django.conf.urls.patterns('',
                (r'^(\d+)/reset-password/$',
                         self.admin_site.admin_view(self.reset_password)
                ),
            )
            return my_urls + urls

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class FamiliePersonFilter (SimpleListFilter):

    	title = 'Personer'
	parameter_name = 'related_person'

	def lookups(self,request,model_admin):
		if request.user.is_superuser:
			lookup_list = list(Person.objects.filter(familie__person__user=request.user).values_list('id','navn')) +[(-1,'===')]+ list(Person.objects.exclude(familie__person__user=request.user).values_list('id','navn'))
		else:
			lookup_list = Person.objects.filter(familie__person__user=request.user).values_list('id','navn')
		return lookup_list

	def queryset(self, request, queryset):
		if self.value():
			person = self.value()
		else:
			try:
				person = request.user.person
			except ObjectDoesNotExist:	
				if request.user.is_superuser:
 					return queryset
				person=None 
		return queryset.filter(person=person)


class UgedagsFilter(SimpleListFilter):
	title = 'Ugedage'
	parameter_name = 'ugedag'

	def lookups(self,request,model_admin):
		return [
		(1,u'Søndag'),
		(2,u'Mandag'),
#		(3,u'Mandag'),
#		(4,u'Onsdag'),
#		(5,u'Torsdag'),
#		(6,u'Fredag'),
#		(7,u'Lørdag'),
		] 

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(maddag__dato__week_day=self.value())
		return queryset

class SnitFilter (SimpleListFilter):
	title = 'Historik'
	parameter_name = 'snit'

	def choices(self, cl):
		return list(super(SnitFilter,self).choices(cl))[1:]

	def lookups(self,request,model_admin):
		return [
		('alle', u'Alle'),
		(None, u'Fremtidige'),
		('hist', u'Historiske'),	
		]

	def queryset(self, request, queryset):
		if self.value()=='hist':
			queryset = queryset.filter(maddag__dato__lt=date.today()).order_by("-maddag__dato")
		elif self.value()==None:
			queryset = queryset.filter(maddag__dato__gte=date.today()-timedelta(days=1)).order_by("maddag__dato")
		return queryset


class MaddagSnitFilter (SimpleListFilter):
	title = 'Historik'
	parameter_name = 'snit'

	def choices(self, cl):
		return list(super(MaddagSnitFilter,self).choices(cl))[1:]

	def lookups(self,request,model_admin):
		return [
		(None, u'Aktuelle'),
		('frem', u'Fremtidige'),
		('hist', u'Historiske'),
		('alle',u'Alle'),
		]

	def queryset(self, request, queryset):
		crit = Q(dato__lt=date.today()) & Q(alle_udlaeg_registreret=True)
		if self.value()=='hist':
			queryset = queryset.filter(dato__lt=date.today()).order_by('-dato')
		elif self.value()=='frem':
			queryset = queryset.filter(dato__gte=date.today()).order_by('dato')
		elif self.value()=='alle':
			queryset = queryset.order_by('-dato')
		else:
			queryset = queryset.filter(~crit).order_by('dato')

		return queryset

class MaanedFilter(SimpleListFilter):
	title = 'Måned'
	parameter_name = 'maaned'

	def lookups(self,request,model_admin):
		return [
		(8,u'August'),
		(9,'September'),
		(10,'Oktober'),
		(11, 'November'),
		(12, 'December'),
		(1, 'Januar')
		]

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(maddag__dato__month=self.value())
		return queryset

class TilmeldingAdmin(admin.ModelAdmin):

	def change_familie(self,request,queryset,value):	
		for t in queryset.all():
			try: 
				for t2 in t.maddag.tilmelding_set.filter(person__familie__person=t.person):
					#Sørg for at t2 og t har samme type - Tilmelding eller AdmTilmelding
					if t.__class__ != t2.__class__:
						t2 = t.__class__.objects.get(pk=t2.pk)
					t2.tilmeldt = value
					t2.save()
			except PermissionDenied:
				from django.contrib import messages
				messages.error(request, "%s: Tilmeldingsfristen er overskredet" % t.maddag.dato )

	def tilmeld_familie(self,request,queryset):
		self.change_familie(request,queryset,True)

	def frameld_familie(self,request,queryset):
		self.change_familie(request,queryset,False)

	def tilmeld(self,request,queryset):
		for t in queryset.all():
			try: 
				t.tilmeldt = True 
				t.save()
			except PermissionDenied:
				from django.contrib import messages
				messages.error(request, "%s: Tilmeldingsfristen er overskredet" % t.maddag.dato )
	
	def frameld(self,request,queryset):
		for t in queryset.all():
			try: 
				t.tilmeldt = False
				t.save()
			except PermissionDenied:
				from django.contrib import messages
				messages.error(request, "%s: Tilmeldingsfristen er overskredet" % t.maddag.dato )

	save_on_top = True

	def menu(self,obj):
		return obj.maddag.vis_menu()
	def madhold(self,obj):
		return obj.maddag.madhold_link() + ' ' + obj.maddag.madhold.mailto_link()

	def mailto_link(self,obj):
		return obj.maddag.madhold.mailto_link()

	mailto_link.allow_tags = True
	madhold.allow_tags = True

	list_display = ['maddag', 'menu','aaben', 'tilmeldt', 'pris', 'tilmeldt_fra_familie', 'gaester_voksne','gaester_boern','pris_aktuel', 'madhold']
	list_editable =  ['tilmeldt', 'gaester_voksne','gaester_boern']
	list_filter = (
		SnitFilter,
		FamiliePersonFilter,
		UgedagsFilter,
		MaanedFilter,
		'maddag__periode',
		)
	readonly_fields = ['pris']
	actions = [tilmeld,tilmeld_familie,frameld, frameld_familie]

	def changelist_view(self, request, extra_context=None):
        	self.list_display_links = (None, )
	        return super(TilmeldingAdmin, self).changelist_view(request, extra_context)

	def get_queryset(self, request):
        	qs = super(TilmeldingAdmin, self).queryset(request).select_related("madhold","madhold__medlemmer")
		u = request.user
	        if u.is_superuser:
	        	return qs
		return qs.filter(Q(person__familie__person__user=u)|Q(maddag__madhold__medlemmer__user=u )).distinct()

	def get_actions(self, request):
        	actions = super(TilmeldingAdmin, self).get_actions(request)
       		if 'delete_selected' in actions:
 	        	del actions['delete_selected']
		if not (request.user.is_superuser or request.user.person.familie.person_set.count()>1):
			del actions ['tilmeld_familie']
			del actions ['frameld_familie']

	        return actions

	def get_model_perms(self, request=None, *args, **kwargs):
		if request.user.is_superuser:
			return {}
		else: 
			return super(TilmeldingAdmin,self).get_model_perms(request,*args,**kwargs)

class AdmTilmeldingAdmin(TilmeldingAdmin):
	def get_model_perms(self, request=None, *args, **kwargs):
		if request.user.is_superuser:
			return super(TilmeldingAdmin,self).get_model_perms(request,*args,**kwargs)
		else: 
			return {}



class UdlaegInline(admin.TabularInline):
	model = Udlaeg 
	fields = ['person', 'beloeb']

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        	field = super(UdlaegInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        	if db_field.name == 'person':
            		if request._obj is not None:
               			field.queryset = field.queryset.filter(madhold = request._obj.madhold).distinct()
            		else:
		                field.queryset = field.queryset.none()
	        return field

class TilmeldingInline(admin.TabularInline):
	model = AdmTilmelding
	fields = ['person', 'tilmeldt', 'gaester_voksne', 'gaester_boern']
	readonly_fields = ['person']
	ordering = ['-tilmeldt','person__familie__husstand','person__familie','person__foedselsdag']
	def has_delete_permission(self,request,obj):
		return False

class MadpraeferencerAdmin(admin.ModelAdmin):
	list_display = ['person', 'fritekst', 'minus_koed','minus_fisk', 'minus_gluten','minus_maelk']
	list_editable = ['fritekst', 'minus_koed','minus_fisk', 'minus_gluten','minus_maelk']

	def get_queryset(self, request):
        	qs = super(MadpraeferencerAdmin, self).get_queryset(request)
	        if request.user.is_superuser:
	        	return qs
		return qs.filter(\
			person__familie__person__user=request.user  
		 ).distinct()


class MaddagAdmin(admin.ModelAdmin):
	date_hierarchy = 'dato'
	list_display = ['detaljer','__unicode__','menu', 'menupris',  'tillad_sen_tilmelding', 'madhold_link', 'tilmeldte_grupper',
	# 'kopier_madhold_fra'
	]
	list_editable = ['menu','menupris', 'tillad_sen_tilmelding',
	# 'kopier_madhold_fra'
	]
	list_filter = [MaddagSnitFilter,]

	fields = ['dato','menupris','menu',  'madhold_link', 'tillad_sen_tilmelding', 'antal_tilmeldte', 'tilmeldte_grupper','tilmeldte_tekst', 'budget', 'alle_udlaeg_registreret',
	# 'kopier_madhold_fra']
	]
	readonly_fields = ['antal_tilmeldte', 'budget',  'tilmeldte_tekst', 'tilmeldte_grupper', 'madhold_link', 'madvanelink']

	inlines = [UdlaegInline,
	# TilmeldingInline
	]

	# Tilføjes kun for superadministrator
	# actions = ['tilfoej_hvis_mangler','genskab_tilmeldinger']

	def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        	request._obj = obj
	        return super(MaddagAdmin, self).get_form(request, obj, **kwargs)

	def get_queryset(self, request):
        	qs = super(MaddagAdmin, self).get_queryset(request)
	        if request.user.is_superuser:
	        	return qs
		return qs.filter(\
			madhold__medlemmer__user=request.user  
		 ).distinct()

	def has_change_permission(self,request,object=None):
		if object == None:
			return True
		if request.user.is_superuser:
			return True
		try:
			p = request.user.person
			if p in object.madhold.medlemmer.all():
				return True
#		except Person.DoesNotExist:
		finally:
			pass
		return False

	def can_change_field(self, request, object, field_name):
		if field_name in ['menu','menupris']:
			return self.has_change_permission(request,object)
		return True


	def tilfoej_hvis_mangler(modeladmin, request, queryset):
		for m in queryset:
			m.tilfoej_hvis_mangler()

	def genskab_tilmeldinger(modeladmin, request, queryset):
		for m in queryset:
			m.genskab_tilmeldinger()

	def get_model_perms(self, request=None, *args, **kwargs):
		if request.user.is_superuser:
			return {}
		else: 
			return super(MaddagAdmin,self).get_model_perms(request,*args,**kwargs)

class AdmMaddagAdmin(MaddagAdmin):
	def get_model_perms(self, request=None, *args, **kwargs):
		if request.user.is_superuser:
			return super(MaddagAdmin,self).get_model_perms(request,*args,**kwargs)
		else:
			return {}
	list_display = ['detaljer','__unicode__','menu', 'menupris',  'tillad_sen_tilmelding', 'madhold_link', 'antal_tilmeldte', 'alle_udlaeg_registreret', 'budget','udlaeg_sum'
	# 'kopier_madhold_fra'
	
	]
	list_editable = ['menu','menupris', 'tillad_sen_tilmelding','alle_udlaeg_registreret'
	# 'kopier_madhold_fra'
	]

class PersonAdmin(admin.ModelAdmin):
	list_display = ['navn','familie', 'foedselsdag', 'prisgruppe', 'telefon', 'user', 'er_beboer', 'madpraeferencer' ]
	list_editable = ['telefon','foedselsdag','er_beboer' ]
	readonly_fields = ['prisgruppe']

#	list_editable = ['familie']
	def get_queryset(self, request):
        	qs = super(PersonAdmin, self).queryset(request)
	        if request.user.is_superuser:
	        	return qs
	        return qs.filter(familie__person__user=request.user)

	def add_to_period(self, request, queryset):
		periode = Periode.objects.filter(slutdato__gte=date.today()).order_by('startdato')[0]
		for person in queryset.all():
			PeriodePerson.objects.get_or_create(periode=periode,person=person)

	def create_user(self, request, queryset):
		for p in queryset.all():
			if p.user == None:
				data = p.navn.replace(' ','')
				u = User.objects.create_user(username=data,email=data,password=data)
				u.groups.add(Group.objects.get(name='Brugere'))
				p.user = u
				p.save()

	actions =[add_to_period,export_as_csv(),create_user]

class PeriodePersonInline(admin.TabularInline):
	model = PeriodePerson

class PeriodeAdmin(admin.ModelAdmin):
	inlines = [PeriodePersonInline]

class PeriodePersonAdmin(admin.ModelAdmin):
	fields = ['person', 'periode', 'deltagelsesprocent'  ]
	list_display = ['person', 'husstand','periode', 'deltagelsesprocent']
	list_filter = ('periode',)
	list_editable =  ['deltagelsesprocent']

	def husstand(self,obj):
		return obj.person.familie.husstand

	def get_queryset(self, request):
        	qs = super(PeriodePersonAdmin, self).queryset(request).order_by('person__familie','person__familie__husstand__adresse')
		return qs

class MadholdAdminForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(MadholdAdminForm, self).__init__(*args, **kwargs)
		instance = kwargs.get('instance', None)
		medlemField = self.fields['medlemmer']
		medlemField.queryset = medlemField.queryset.order_by('navn')

class UdlaegAdmin(admin.ModelAdmin):

	list_display = ['maddag', 'person', 'beloeb', 'afregnet']
	list_editable = ['afregnet']

	def get_model_perms(self, request):
	        """
        	Return empty perms dict thus hiding the model from admin index.
	        """
		u = request.user
		if u.is_superuser:
			return super(UdlaegAdmin,self).get_model_perms(request)
		else:
        		return {}

class MadholdAdmin(admin.ModelAdmin):

	def get_model_perms(self, request):
	        """
        	Return empty perms dict thus hiding the model from admin index.
	        """
		u = request.user
		if u.is_superuser:
			return super(MadholdAdmin,self).get_model_perms(request)
		else:
        		return {}

	filter_horizontal = ['medlemmer']
	form = MadholdAdminForm
	list_display = ['navn','medlemsliste']

	def has_change_permission(self, request, madhold=None):
		if request.user.is_superuser:
			return True
		if not madhold:
			return False
		try:
			p = request.user.person
			if p in madhold.medlemmer.all():
				return True
#		except Person.DoesNotExist:
		finally:
			pass
		return False

	def response_change(self, request, obj, post_url_continue=None):
		from django.core.urlresolvers import reverse
		from django.http import HttpResponseRedirect
		"""This makes the response after adding go to another apps changelist for some model"""

		if request.user.is_superuser:
			return HttpResponseRedirect(reverse("admin:madplan_admmaddag_changelist"))
		else:
			return HttpResponseRedirect(reverse("admin:madplan_maddag_changelist"))
			

class PersonInline(admin.TabularInline):
	def has_add_permission(self, request):
		return True	
	model = Person
	fields = ['navn', 'foedselsdag']
	

class HusstandAdmin(admin.ModelAdmin):
	list_display = ['adresse',]


class FamilieAdmin(admin.ModelAdmin):
	def split(self, request, queryset):
		for q in queryset:
			q.split()

	def join (self,request,queryset):
		if len(queryset) > 1:
			fk = queryset[0]
			for f in queryset[1:]:
				f.person_set.update(familie=fk)
				f.delete()
	
	def add_to_period(self, request, queryset):
		periode = Periode.objects.filter(slutdato__gte=date.today()).order_by('startdato')[0]
		for family in queryset:
			for person in family.person_set.all():
				PeriodePerson.objects.get_or_create(periode=periode,person=person)
				

	actions = [split, join, add_to_period]
	inlines = [PersonInline,]
		

admin.site.register(Madpraeferencer, MadpraeferencerAdmin)
admin.site.register(Maddag, MaddagAdmin)
admin.site.register(AdmMaddag, AdmMaddagAdmin)
admin.site.register(Udlaeg, UdlaegAdmin)
admin.site.register(Madhold, MadholdAdmin)
admin.site.register(Periode, PeriodeAdmin)
admin.site.register(PeriodePerson, PeriodePersonAdmin)
admin.site.register(Tilmelding, TilmeldingAdmin)
admin.site.register(AdmTilmelding, AdmTilmeldingAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Husstand, HusstandAdmin)
admin.site.register(Familie, FamilieAdmin)
	

