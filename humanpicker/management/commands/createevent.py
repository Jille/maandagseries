from django.core.management.base import BaseCommand, CommandError

from maandagseries.humanpicker.models import Event
from maandagseries.util import parse_date

class Command(BaseCommand):
	args = '<date> [places]'
	help = 'Create a new event'

	def handle(self, *args, **options):
		if len(args) < 1 or len(args) > 2:
			raise CommandError("Usage: createevent %s" % self.args)
		ev = Event(date=parse_date(args[0]))
		if len(args) == 2:
			ev.places = int(args[1])
		ev.save()
