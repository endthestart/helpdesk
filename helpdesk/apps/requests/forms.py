from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.formtools.wizard import FormWizard
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.translation import ugettext

from requests.models import Category, Ticket, EnvironmentDetails

PRIORITY_CHOICES = (
        ("5", "General Question"),
        ("4", "Low Priority"),
        ("3", "Moderate Priority"),
        ("2", "High Priority"),
        ("1", "Need Help Now"),
    )

class EnvironmentDetailsForm(forms.Form):
    other_environment = forms.BooleanField(required=False)
    operating_system = forms.CharField(max_length=255, required=False)
    screen_resolution = forms.CharField(max_length=30, required=False)
    browser = forms.CharField(max_length=255, required=False)
    browser_size = forms.CharField(max_length=30, required=False)
    ip_address = forms.CharField(max_length=15, required=False)
    color_depth = forms.IntegerField(required=False)
    javascript = forms.BooleanField(required=False)
    flash_version = forms.FloatField(required=False)
    cookies = forms.BooleanField(required=False)

class RequestForm(forms.Form):
    category = forms.ModelChoiceField(Category.objects.all())
    priority = forms.ChoiceField(choices=Ticket.PRIORITY_CHOICES)
    short_description = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, max_length=1000)


class RequestWizard(FormWizard):
    @transaction.commit_on_success
    def done(self, request, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)

        if data["other_environment"]:
            environment_details = None
        else:
            environment_details = EnvironmentDetails.objects.create(
                operating_system = data["operating_system"],
                screen_resolution = data["screen_resolution"],
                browser =  data["browser"],
                browser_size = data["browser_size"],
                ip_address = data["ip_address"],
                color_depth = data["color_depth"],
                javascript = data["javascript"],
                flash_version = data["flash_version"],
                cookies = data["cookies"]
            )

        ticket = Ticket(
            user = request.user,
            category = data["category"],
            priority = data["priority"],
            short_description = data["short_description"],
            description = data["description"],
            state = 1,
            environment_details = environment_details,
            assigned_user = None,
            closed = None
        )
        ticket.save()
        messages.add_message(request, messages.SUCCESS, ugettext(u"Ticket successfully submitted."))
        return HttpResponseRedirect("/requests/open/")

    def get_template(self, step):
        return "requests/new.html"