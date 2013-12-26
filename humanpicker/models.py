import hashlib

from django.db import models

from maandagseries import settings

class Event(models.Model):
	date = models.DateField(unique=True)
	places = models.PositiveSmallIntegerField()
	open = models.BooleanField(default=False)
	chef = models.CharField("CHEF", max_length=32, blank=True, null=True)

	def getKey(self):
		return hashlib.md5("%s-%s" % (self.date, settings.SECRET_KEY)).hexdigest()

	def __unicode__(self):
		return str(self.date)

	@models.permalink
	def get_absolute_url(self):
		return ('subscribe', (), {'date': str(self.date), 'key': self.getKey()})

class Human(models.Model):
	event = models.ForeignKey(Event)
	name = models.CharField("naam", max_length=32)
	subscribed_at = models.DateTimeField(auto_now_add=True)
	subscribed_by = models.IPAddressField()
	is_creative = models.BooleanField("Wil een gerecht verzinnen")
	accepted = models.BooleanField("Mag komen")

	def __unicode__(self):
		return "%s op %s" % (self.name, self.event)

	class Meta:
		unique_together = (('event', 'name'), )

class Furniture(models.Model):
	name = models.CharField("naam", max_length=32)
	is_creative = models.BooleanField("Wil een gerecht verzinnen")

	def __unicode__(self):
		return self.name
