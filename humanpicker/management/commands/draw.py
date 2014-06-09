import datetime
import random
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage

from maandagseries.humanpicker.models import Event, Human

def pick_one_from_scores(scores):
	total = 0
	for k, v in scores.items():
		total += v
	winner = random.randint(0, total)
	for k, v in scores.items():
		if winner < v:
			return k
		winner -= v
	offByOneBug()

class Command(BaseCommand):
	args = '[-f]'
	help = 'Draw some random names'
	option_list = BaseCommand.option_list + (
		make_option('-f',
		action='store_true',
		dest='forcePick',
		default=False,
		help='Force picking the chef and souschef'),
	)

	def handle(self, *args, **options):
		if len(args) != 0:
			raise CommandError("Usage: draw %s" % self.args)
		for ev in Event.objects.filter(open=True):
			already_accepted = map(lambda x: x.name, Human.objects.filter(event=ev, accepted=True, revoked=False))
			places = ev.places - len(already_accepted)
			new_names = []
			mailworthy = False
			if places > 0:
				humans = dict((x.id, x) for x in (Human.objects.filter(event=ev, accepted=False, revoked=False)))
				if len(humans) > 0:
					scores = {}
					for hid, human in humans.items():
						scores[hid] = 100
						if human.is_creative:
							scores[hid] += 25
					while places > 0 and len(scores) > 0:
						hid = pick_one_from_scores(scores)
						humans[hid].accepted = True
						humans[hid].save()
						del scores[hid]
						places -= 1
						new_names.append(humans[hid].name)
						mailworthy = True
			if (places <= 0 or options['forcePick']) and ev.chef is None:
				chefs = Human.objects.filter(event=ev, accepted=True, revoked=False, is_creative=True))
				ev.chef = random.choice(chefs).name
				ev.save()
				mailworthy = True
			if (places <= 0 or options['forcePick']) and ev.souschef is None:
				souschefs = Human.objects.filter(event=ev, accepted=True, revoked=False).exclude(name=ev.chef)
				ev.souschef = random.choice(souschefs).name
				ev.save()
				mailworthy = True

			if not mailworthy:
				continue

			msgparts = []
			if len(new_names) > 0:
				msg = ""
				if len(new_names) == 1:
					msg += "%s is ingeloot" % new_names[0]
				else:
					last = new_names.pop()
					msg += "%s en %s zijn ingeloot" % (", ".join(new_names), last)

				if len(already_accepted) == 1:
					msg += " (naast %s)" % already_accepted[0]
				elif len(already_accepted) > 1:
					last = already_accepted.pop()
					msg += " (naast %s en %s)" % (", ".join(already_accepted), last)
				msgparts.append(msg)

			if places == 1:
				msgparts.append("Er is nog een plek. Meld je snel aan op:\nhttp://maandagseries.quis.cx"+ ev.get_absolute_url())
			elif places > 1:
				msgparts.append("Er zijn nog %d plaatsen. Meld je snel aan op:\nhttp://maandagseries.quis.cx%s" % (places, ev.get_absolute_url()))

			if not ev.chef is None:
				msg = "%s mag een gerecht verzinnen." % ev.chef
				if not ev.souschef is None:
					msg += " %s mag helpen met boodschappen doen." % ev.souschef
				msgparts.append(msg)

			msg = "\n\n".join(msgparts)
			headers = {'In-Reply-To': "<%s@maandagseries.quis.cx>" % ev.getKey(), 'References': "<%s@maandagseries.quis.cx>" % ev.getKey()}
			email = EmailMessage('Re: %s' % ev.date.strftime('%e %b'), msg, 'maandagseries@karpenoktem.nl', ['maandagseries@karpenoktem.nl'], headers=headers)
			email.send()
