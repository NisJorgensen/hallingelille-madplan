from django.contrib import admin

admin.autodiscover()

from django.conf.urls import patterns, include, url


urlpatterns = patterns ('',
    # Examples:
    # url(r'^$', 'hallingelille.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^', include('hallingelille.madplan.urls')),
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
    'django.contrib.auth.views.password_reset_confirm',
    name='password_reset_confirm'),
    url (r'^reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^become/(.*)$', 'hallingelille.views.become' ),

    url (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/accounts/password/reset/done/'}),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url (r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',  {'post_reset_redirect' : '/accounts/password/complete/'}),
    url(r'^accounts/password/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^boern$', 'hallingelille.views.boerneliste', name='boerneliste'),
)
