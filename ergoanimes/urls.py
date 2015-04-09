# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^$', views.anime_list, name='index'),

    url(r'^anime/$', views.anime_list, name='anime_list'),
    url(r'^anime/season/$', views.anime_byseason, name='anime_byseason'),
    url(r'^anime/add/$', views.anime_form, name='anime_add'),
    url(r'^anime/(?P<pk>\d+)/$', views.anime_show, name='anime'),
    url(r'^anime/(?P<pk>\d+)/edit/$', views.anime_form, name='anime_edit'),
    url(r'^anime/(?P<pk>\d+)/delete/$', views.anime_delete, name='anime_delete'),

    url(r'^fansub/$', views.fansub_list, name='fansub_list'),
    url(r'^fansub/add/$', views.fansub_form, name='fansub_add'),
    url(r'^fansub/(?P<pk>\d+)/$', views.fansub_show, name='fansub'),
    url(r'^fansub/(?P<pk>\d+)/edit/$', views.fansub_form, name='fansub_edit'),
    url(r'^fansub/(?P<pk>\d+)/delete/$', views.fansub_delete, name='fansub_delete'),

    url(r'^genre/$', views.genre_list, name='genre_list'),
    url(r'^genre/(?P<pk>\d+)/$', views.genre_show, name='genre'),

    url(r'^anime/user/$', views.useranime_list, name='useranime_list'),
    url(r'^anime/status/$', views.useranime_status, name='useranime_status'),
    url(r'^anime/reports/$', views.useranime_reports, name='useranime_reports'),
    url(r'^anime/check/$', views.useranime_check, name='useranime_check'),
    url(r'^anime/note/$', views.useranime_bynote, name='useranime_bynote'),
    url(r'^anime/viewedhd/$', views.useranime_viewedhd, name='useranime_viewedhd'),
    url(r'^anime/(?P<pk>\d+)/user/$', views.useranime_form, name='useranime_form'),
    url(r'^anime/(?P<pk>\d+)/user/delete/$', views.useranime_delete, name='useranime_delete'),
    url(r'^anime/(?P<pk>\d+)/plus/(?P<episode_type>\w+)/$', views.useranime_plus, name='useranime_plus'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergoanimes')),
]
