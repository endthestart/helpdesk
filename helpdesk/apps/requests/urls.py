from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from requests.forms import RequestForm, EnvironmentDetailsForm, RequestWizard


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "requests/requests.html"}, name="requests"),
    url(r"^new/$", RequestWizard([EnvironmentDetailsForm, RequestForm]), name="request_new"),
    url(r"^open/$", "requests.views.open_requests", name="request_open"),
    #url(r"^closed/$", "requests.views.closed_requests", name="request_closed"),
)
