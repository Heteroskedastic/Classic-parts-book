from django.conf.urls import patterns, url

from maps.views import (HomeView, ImageMapView, AddPartsView, MapCreate,
                        UploadBook, BookPageView, MotorcycleView)

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name='home'),
                       url(r'^tool/$', ImageMapView.as_view(),
                           name='image_map'),
                       url(r'^upload_book/$', UploadBook.as_view(),
                           name='upload_book'),
                       url(r'^add_parts/(?P<id>\d+)/$', AddPartsView.as_view(),
                           name='add_part'),
                       url(r'^map_attr/$', MapCreate.as_view(),
                           name='map_create'),
                       url(r'^book/(?P<book_id>\d+)/$', BookPageView.as_view(),
                           name='book_view'),
                       url(r'^book/(?P<book_id>\d+)/(?P<page_id>\d+)$', BookPageView.as_view(),
                           name='book_page_view'),
                       url(r'^motorcycle/(?P<moto_id>\d+)/$', MotorcycleView.as_view(),
                           name='motorcycle_view'),
                       # url(r'^create_part/$', PartCreate.as_view(),
                       #     name='part_create'),

                       )
