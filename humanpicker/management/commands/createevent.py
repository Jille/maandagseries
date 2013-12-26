from django.core.management.base import BaseCommand, CommandError

from maandagseries.humanpicker.models import Event, Human, Furniture
from maandagseries.util import parse_date

class Command(BaseCommand):
	args = '<date> <places>'
	help = 'Create a new event'

	def handle(self, *args, **options):
		if len(args) != 2:
			raise CommandError("Usage: createevent %s" % self.args)
		ev = Event(date=parse_date(args[0]))
		ev.places = int(args[1])
		ev.save()
		for f in Furniture.objects.all():
			human = Human()
			human.event = ev
			human.name = f.name
			human.is_creative = f.is_creative
			human.accepted = True
			human.subscribed_by = '127.0.0.1'
			human.save()
