from django.conf.urls import patterns, url

from maps.views import *

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^tool/$', ImageMapView.as_view(),
                           name='image_map'),
                       url(r'^images/$', ShowImageView.as_view(),
                           name='image_show'),
                       url(r'^add_parts/(?P<id>\d+)/$', AddPartsView.as_view(),
                           name='add_part'),
                       url(r'^map_attr/$', MapCreate.as_view(),
                           name='map_create'),
                       # url(r'^create_part/$', PartCreate.as_view(),
                       #     name='part_create'),

                       )
