from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from maandagseries.humanpicker.models import Event, Human
from maandagseries.humanpicker.forms import SubscribeForm

def home(request):
	return render_to_response('home.html', context_instance=RequestContext(request))

def subscribe(request, date, key):
	try:
		ev = Event.objects.get(date=date)
	except:
		raise Http404
	if ev.getKey() != key or not ev.open:
		raise PermissionDenied

	human = Human(event=ev, subscribed_by=request.META.get('REMOTE_ADDR'))

	if request.method == 'POST':
		form = SubscribeForm(request.POST, instance=human)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("gaaf/")
	else:
		form = SubscribeForm(instance=human)
	return render_to_response('subscribe.html', {'ev': ev, 'form': form}, context_instance=RequestContext(request))

def subscribed(request, date, key):
	try:
		ev = Event.objects.get(date=date)
	except:
		raise Http404
	if ev.getKey() != key or not ev.open:
		raise PermissionDenied

	return render_to_response('subscribed.html', {'ev': ev}, context_instance=RequestContext(request))
