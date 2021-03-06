from django.contrib import admin
from django.contrib.auth.models import Group

from maandagseries.humanpicker.models import Event, Human, Furniture

class EventAdmin(admin.ModelAdmin):
	list_display = ('date', 'places', 'open', 'chef', 'souschef')
	list_filter = ('open', 'places', 'chef', 'souschef')
	ordering = ('date', )
	date_hierarchy = 'date'

class HumanAdmin(admin.ModelAdmin):
	list_display = ('name', 'event', 'accepted', 'revoked', 'is_creative', 'subscribed_at', 'subscribed_by')
	list_filter = ('accepted', 'revoked', 'is_creative', 'name', 'event')
	ordering = ('event', 'subscribed_at')
	actions = ['accept', 'unaccept', 'revoke', 'unrevoke']

	def accept(self, request, queryset):
		queryset.update(accepted=True)
	accept.short_description = 'Accept selected humans'

	def unaccept(self, request, queryset):
		queryset.update(accepted=False)
	unaccept.short_description = 'Unaccept selected humans'

	def revoke(self, request, queryset):
		queryset.update(revoked=True)
	revoke.short_description = 'Revoke selected humans'

	def unrevoke(self, request, queryset):
		queryset.update(revoked=False)
	unrevoke.short_description = 'Unrevoke selected humans'

class FurnitureAdmin(admin.ModelAdmin):
	list_display = ('name', 'is_creative')
	ordering = ('name',)

admin.site.register(Event, EventAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.register(Furniture, FurnitureAdmin)
admin.site.unregister(Group)
