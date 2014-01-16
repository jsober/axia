from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^station_report/$', 'vo.econ.views.station_report'),
    url(r'^nearest_items/$', 'vo.econ.views.nearest_sale_locations'),
    url(r'^cheapest_items/$', 'vo.econ.views.cheapest_sale_locations'),
)
