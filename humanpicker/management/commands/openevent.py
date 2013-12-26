from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage

from maandagseries.humanpicker.models import Event
from maandagseries.util import parse_date

class Command(BaseCommand):
	args = '<date>'
	help = 'Open an event'

	def handle(self, *args, **options):
		if len(args) != 1:
			raise CommandError("Usage: openevent %s" % self.args)
		ev = Event.objects.get(date=parse_date(args[0]))
		ev.open = True
		ev.save()
		if ev.places > 0:
			msg = "Er zijn %d plaatsen. Meld je snel aan op:\nhttp://maandagseries.quis.cx%s" % (ev.places, ev.get_absolute_url())
			headers = {'Message-Id': "%s@maandagseries.quis.cx" % ev.getKey()}
			email = EmailMessage('%s' % ev.date.strftime('%e %b'), msg, 'maandagseries@karpenoktem.nl', ['jille@karpenoktem.nl'], headers=headers)
			email.send()
