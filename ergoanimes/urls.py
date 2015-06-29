# -*- coding: utf-8 -*-
#
# Copyright 2015 Eduardo Augusto Klosowski
#
# This file is part of Ergo Animes.
#
# Ergo Animes is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ergo Animes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Ergo Animes.  If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls import include, url

from . import views


url_list = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^anime/$', views.AnimeListView.as_view(), name='anime_list'),
    url(r'^anime/season/$', views.AnimeSeasonListView.as_view(), name='anime_seasonlist'),
    url(r'^anime/(?P<pk>\d+)/$', views.AnimeDetailView.as_view(), name='anime'),
    url(r'^anime/add/$', views.AnimeCreateView.as_view(), name='anime_add'),
    url(r'^anime/(?P<pk>\d+)/edit/$', views.AnimeUpdateView.as_view(), name='anime_edit'),
    url(r'^anime/(?P<pk>\d+)/delete/$', views.AnimeDeleteView.as_view(), name='anime_delete'),

    url(r'^fansub/$', views.FansubListView.as_view(), name='fansub_list'),
    url(r'^fansub/(?P<pk>\d+)/$', views.FansubDetailView.as_view(), name='fansub'),
    url(r'^fansub/add/$', views.FansubCreateView.as_view(), name='fansub_add'),
    url(r'^fansub/(?P<pk>\d+)/edit/$', views.FansubUpdateView.as_view(), name='fansub_edit'),
    url(r'^fansub/(?P<pk>\d+)/delete/$', views.FansubDeleteView.as_view(), name='fansub_delete'),

    url(r'^genre/$', views.GenreListView.as_view(), name='genre_list'),
    url(r'^genre/(?P<pk>\d+)/$', views.GenreDetailView.as_view(), name='genre'),

    url(r'^anime/user/$', views.UserAnimeListView.as_view(), name='useranime_list'),
    url(r'^anime/user/status/$', views.UserAnimeStatusListView.as_view(), name='useranime_statuslist'),
    url(r'^anime/user/report/$', views.UserAnimeReportListView.as_view(), name='useranime_reportlist'),
    url(r'^anime/user/checknew/$', views.UserAnimeCheckNewListView.as_view(), name='useranime_checknewlist'),
    url(r'^anime/(?P<pk>\d+)/user/add/$', views.UserAnimeCreateView.as_view(), name='useranime_add'),
    url(r'^anime/(?P<pk>\d+)/user/edit/$', views.UserAnimeUpdateView.as_view(), name='useranime_edit'),
    url(r'^anime/(?P<pk>\d+)/user/delete/$', views.UserAnimeDeleteView.as_view(), name='useranime_delete'),
    url(r'^anime/(?P<pk>\d+)/plus/(?P<episode_type>\w+)/$', views.UserAnimePlusView.as_view(), name='useranime_plus'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergoanimes')),
]
