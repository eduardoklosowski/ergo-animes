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
    url(r'^fansub/$', views.FansubListView.as_view(), name='fansub_list'),
    url(r'^fansub/(?P<pk>\d+)/$', views.FansubDetailView.as_view(), name='fansub'),
    url(r'^fansub/add/$', views.FansubCreateView.as_view(), name='fansub_add'),
    url(r'^fansub/(?P<pk>\d+)/edit/$', views.FansubUpdateView.as_view(), name='fansub_edit'),
    url(r'^fansub/(?P<pk>\d+)/delete/$', views.FansubDeleteView.as_view(), name='fansub_delete'),

    url(r'^genre/$', views.GenreListView.as_view(), name='genre_list'),
]

urlpatterns = [
    url('', include(url_list, namespace='ergoanimes')),
]
