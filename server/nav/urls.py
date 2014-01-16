from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^sector_report/$', 'vo.nav.views.sector_report'),
    url(r'^plot/$', 'vo.nav.views.plot'),
    url(r'^storms/$', 'vo.nav.views.list_storms'),
)
