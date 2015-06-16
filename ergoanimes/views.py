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

from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.functions import Lower
from django.views import generic
from ergo.views import LoginRequiredMixin, PermissionRequiredMixin
from userviews import views as userviews

from . import models


# Anime

class AnimeListView(LoginRequiredMixin, generic.ListView):
    model = models.Anime
    ordering = (Lower('name'),)

    def get_queryset(self):
        qs = super(AnimeListView, self).get_queryset()
        for word in self.request.GET.get('anime', '').split():
            qs = qs.filter(name__icontains=word)
        return qs.prefetch_related('genres')


class AnimeDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Anime

    def get_queryset(self):
        qs = super(AnimeDetailView, self).get_queryset()
        return qs.prefetch_related('genres')

    def get_context_data(self, **kwargs):
        try:
            useranime = self.object.useranimes.filter(user=self.request.user).select_related('fansub').get()
        except ObjectDoesNotExist:
            useranime = None

        context = super(AnimeDetailView, self).get_context_data(**kwargs)
        context['useranime'] = useranime
        return context


class AnimeCreateView(PermissionRequiredMixin, generic.CreateView):
    permission = 'ergoanimes.add_anime'
    model = models.Anime
    fields = ('name', 'media_type', 'img', 'episodes', 'duration', 'air_start', 'air_end',
              'season_start', 'season_end', 'genres', 'mal', 'anidb', 'synopsis')


class AnimeUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission = 'ergoanimes.change_anime'
    model = models.Anime
    fields = ('name', 'media_type', 'img', 'episodes', 'duration', 'air_start', 'air_end',
              'season_start', 'season_end', 'genres', 'mal', 'anidb', 'synopsis')


class AnimeDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission = 'ergoanimes.delete_anime'
    model = models.Anime
    success_url = reverse_lazy('ergoanimes:anime_list')


# Fansub

class FansubListView(LoginRequiredMixin, generic.ListView):
    model = models.Fansub


class FansubDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Fansub


class FansubCreateView(PermissionRequiredMixin, generic.CreateView):
    permission = 'ergoanimes.add_fansub'
    model = models.Fansub
    fields = ('name', 'site', 'irc', 'active', 'img')


class FansubUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission = 'ergoanimes.change_fansub'
    model = models.Fansub
    fields = ('name', 'site', 'irc', 'active', 'img')


class FansubDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission = 'ergoanimes.delete_fansub'
    model = models.Fansub
    success_url = reverse_lazy('ergoanimes:fansub_list')


# Genre

class GenreListView(LoginRequiredMixin, generic.ListView):
    model = models.Genre
    template_name = 'ergoanimes/genre_list.html'
    context_object_name = 'genre_list'

    def get_queryset(self):
        qs = super(GenreListView, self).get_queryset()
        return sorted(qs, key=lambda x: x.get_genre_display())


class GenreDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Genre


# UserAnime

class UserAnimeListView(LoginRequiredMixin, userviews.UserListView):
    model = models.UserAnime
    ordering = (Lower('anime__name'),)

    def get_queryset(self):
        qs = super(UserAnimeListView, self).get_queryset()
        return qs.select_related('anime', 'fansub')


class UserAnimeCreateView(LoginRequiredMixin, userviews.SharedUserCreateView):
    model = models.UserAnime
    shared_model = models.Anime
    fields = ('user', 'anime', 'status', 'fansub', 'quality', 'resolution', 'episodes_pub', 'episodes_down',
              'episodes_viewed', 'times', 'date_start', 'date_end', 'link', 'note', 'comment')


class UserAnimeUpdateView(LoginRequiredMixin, userviews.SharedUserUpdateView):
    model = models.UserAnime
    shared_model = models.Anime
    fields = ('status', 'fansub', 'quality', 'resolution', 'episodes_pub', 'episodes_down',
              'episodes_viewed', 'times', 'date_start', 'date_end', 'link', 'note', 'comment')

    def get_queryset(self):
        qs = super(UserAnimeUpdateView, self).get_queryset()
        return qs.select_related('anime', 'fansub')


class UserAnimeDeleteView(LoginRequiredMixin, userviews.SharedUserDeleteView):
    model = models.UserAnime
    shared_model = models.Anime

    def get_queryset(self):
        qs = super(UserAnimeDeleteView, self).get_queryset()
        return qs.select_related('anime')

    def get_success_url(self):
        return reverse('ergoanimes:anime', args=(self.kwargs['pk'],))
