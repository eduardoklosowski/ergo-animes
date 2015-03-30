# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^fansub/$', views.fansub_list, name='fansub_list'),
    url(r'^fansub/add/$', views.fansub_form, name='fansub_add'),
    url(r'^fansub/(?P<pk>\d+)/$', views.fansub_show, name='fansub'),
    url(r'^fansub/(?P<pk>\d+)/edit/$', views.fansub_form, name='fansub_edit'),
    url(r'^fansub/(?P<pk>\d+)/delete/$', views.fansub_delete, name='fansub_delete'),

    url(r'^genre/$', views.genre_list, name='genre_list'),
    url(r'^genre/(?P<pk>\d+)/$', views.genre_show, name='genre'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergoanimes')),
]
