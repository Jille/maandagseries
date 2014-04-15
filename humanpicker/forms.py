from django.forms import ModelForm, ValidationError

from maandagseries.humanpicker.models import Human

class SubscribeForm(ModelForm):
	class Meta:
		model = Human
		exclude = ['event', 'subscribed_by', 'accepted', 'revoked']
	def clean(self):
		res = Human.objects.filter(event=self.instance.event, name=self.cleaned_data['name']).count()
		if res > 0:
			raise ValidationError(["%s is al ingeschreven" % self.cleaned_data['name']])
		return self.cleaned_data
