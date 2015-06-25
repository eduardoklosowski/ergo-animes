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
from django.db.models import Count
from django.db.models.functions import Lower
from django.views import generic
from ergo.views import LoginRequiredMixin, PermissionRequiredMixin
from userviews import views as userviews

from . import models


class IndexView(LoginRequiredMixin, generic.RedirectView):
    permanent = False
    url = reverse_lazy('ergoanimes:useranime_statuslist')


# Anime

class AnimeListView(LoginRequiredMixin, generic.ListView):
    model = models.Anime
    ordering = (Lower('name'),)

    def get_queryset(self):
        qs = super(AnimeListView, self).get_queryset()
        for word in self.request.GET.get('anime', '').split():
            qs = qs.filter(name__icontains=word)
        return qs.prefetch_related('genres')

    def get_context_data(self, **kwargs):
        anime_status = dict(models.UserAnime.objects.filter(user=self.request.user).values_list('anime', 'status'))

        context = super(AnimeListView, self).get_context_data(**kwargs)
        context['anime_status'] = anime_status
        return context


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

    def get_context_data(self, **kwargs):
        mylist_count = dict(models.UserAnime.objects.filter(user=self.request.user, fansub__isnull=False)
                            .order_by().values_list('fansub').annotate(count=Count(1)))

        context = super(FansubListView, self).get_context_data(**kwargs)
        context['mylist_count'] = mylist_count
        return context


class FansubDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Fansub

    def get_context_data(self, **kwargs):
        mylist_list = models.Anime.objects.filter(
            pk__in=models.UserAnime.objects.filter(user=self.request.user, fansub=self.object)
            .values_list('anime', flat=True),
        )

        context = super(FansubDetailView, self).get_context_data(**kwargs)
        context['mylist_list'] = mylist_list
        return context


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

    def get_context_data(self, **kwargs):
        anime_count = dict(models.Genre.objects.order_by().values_list('genre').annotate(count=Count('animes')))
        mylist_count = dict(models.Genre.objects.order_by().values_list('genre').filter(
            animes__in=models.UserAnime.objects.filter(user=self.request.user).values_list('anime', flat=True),
        ).annotate(count=Count('animes')))

        context = super(GenreListView, self).get_context_data(**kwargs)
        context['anime_count'] = anime_count
        context['mylist_count'] = mylist_count
        return context


class GenreDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Genre

    def get_context_data(self, **kwargs):
        anime_list = self.get_object().animes.all()
        mylist_list = self.get_object().animes.filter(
            pk__in=models.UserAnime.objects.filter(user=self.request.user).values_list('anime', flat=True),
        )

        context = super(GenreDetailView, self).get_context_data(**kwargs)
        context['anime_list'] = anime_list
        context['mylist_list'] = mylist_list
        return context


# UserAnime

class UserAnimeListView(LoginRequiredMixin, userviews.UserListView):
    model = models.UserAnime
    ordering = (Lower('anime__name'),)

    def get_queryset(self):
        qs = super(UserAnimeListView, self).get_queryset()
        return qs.select_related('anime', 'fansub')


class UserAnimeStatusListView(LoginRequiredMixin, userviews.UserListView):
    model = models.UserAnime
    ordering = (Lower('anime__name'),)
    template_name_suffix = '_statuslist'

    def get_queryset(self):
        qs = super(UserAnimeStatusListView, self).get_queryset()
        return qs.select_related('anime', 'fansub')

    def get_context_data(self, **kwargs):
        qs = self.object_list
        status_list = [(status_id, status, [useranime for useranime in qs if useranime.status == status_id])
                       for status_id, status in models.CHOICES_STATUS[1:] + models.CHOICES_STATUS[:1]]

        context = super(UserAnimeStatusListView, self).get_context_data(**kwargs)
        context['status_list'] = status_list
        return context


class UserAnimeReportListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ergoanimes/useranime_reportlist.html'

    def get_context_data(self, **kwargs):
        report_list = [
            ('watch', 'Assistir',
             models.UserAnime.objects.watch(self.request.user).select_related('fansub')),
            ('down', 'Baixar',
             models.UserAnime.objects.down(self.request.user).select_related('fansub')),
            ('new-watch', 'Novos para Assistir',
             models.UserAnime.objects.new_watch(self.request.user).select_related('fansub')),
            ('new-down', 'Novos para Baixar',
             models.UserAnime.objects.new_down(self.request.user).select_related('fansub')),
        ]

        context = super(UserAnimeReportListView, self).get_context_data(**kwargs)
        context['report_list'] = report_list
        return context


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
