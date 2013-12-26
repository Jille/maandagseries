from django.contrib import admin
from django.contrib.auth.models import Group

from maandagseries.humanpicker.models import Event, Human

class EventAdmin(admin.ModelAdmin):
	list_display = ('date', 'places', 'open')
	ordering = ('date', )

class HumanAdmin(admin.ModelAdmin):
	list_display = ('name', 'event', 'accepted', 'is_creative', 'subscribed_at', 'subscribed_by')
	ordering = ('event', 'subscribed_at')
	actions = ['accept', 'unaccept']

	def accept(self, request, queryset):
		queryset.update(accepted=True)
	accept.short_description = 'Accept selected humans'

	def unaccept(self, request, queryset):
		queryset.update(accepted=False)
	unaccept.short_description = 'Unaccept selected humans'

admin.site.register(Event, EventAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.unregister(Group)
