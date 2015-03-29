# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^genre/$', views.genre_list, name='genre_list'),
    url(r'^genre/(?P<pk>\d+)/$', views.genre_show, name='genre'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergoanimes')),
]
