from django.contrib import admin

from requests.models import Ticket, Category


admin.site.register(Ticket)
admin.site.register(Category)