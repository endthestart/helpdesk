from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required

from requests.models import Ticket

#@login_required
#def new_request(request, template_name="requests/new.html"):
#    if request.method == "POST":
#        form = RequestForm(request.user, request.POST, request.FILES)
#        if form.is_valid():
#            ticket = form.save()
#            messages.add_message(request, messages.SUCCESS,
#                                 ugettext(u"Ticket successfully submitted.")
#            )
#            return HttpResponseRedirect("/requests/done/")
#    else:
#        form = RequestForm(request.user)
#        c = {"form": form}
#    return render_to_response(template_name, RequestContext(request, c))

@login_required
def open_requests(request, template_name="requests/open.html"):
    tickets = Ticket.objects.filter(user=request.user)
    c = {"tickets": tickets}
    return render_to_response(template_name, RequestContext(request, c))