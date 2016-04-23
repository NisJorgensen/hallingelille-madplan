from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from hallingelille.madplan import views
from kalender import MaddagFeed

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hallingelille.views.home', name='home'),
    # url(r'^hallingelille/', include('hallingelille.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.index),
    url(r'^afregning$', views.afregning, name='afregning'),
    url(r'^afregning_udlaeg$', views.afregning_udlaeg, name='afregning_udlaeg'),
    url(r'^kalender.*', MaddagFeed()),
    url(r'^maddag/([0-9]{4}-[0-9]{2}-[0-9]{2})$', views.maddag),
    url(r'^madvaner$', views.madvaner),
    url(r'^madvaner/([0-9]{4}-[0-9]{2}-[0-9]{2})$', views.madvaner_for_dato)
)
