from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'maandagseries.humanpicker.views.home', name='home'),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<key>[a-f0-9]{32})/$', 'maandagseries.humanpicker.views.subscribe', name='subscribe'),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<key>[a-f0-9]{32})/gaaf/$', 'maandagseries.humanpicker.views.subscribed', name='subscribed'),

    url(r'^admin/', include(admin.site.urls)),
)
