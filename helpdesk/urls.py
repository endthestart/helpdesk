from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', direct_to_template, { "template": "homepage.html",}, name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', include("helpdesk.about.urls")),
)
