# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import defaultdict
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from ergo.genericview import DeleteView

from . import reports
from .forms import AnimeForm, FansubForm, UserAnimeForm
from .models import Anime, Fansub, Genre, UserAnime, CHOICES_STATUS
from .tables import (AnimeTable, FansubTable, GenreTable, UserAnimeTable, UserAnimeStatusTable,
                     UserAnimeDownTable, UserAnimePubTable)
from .utils import add_down, add_pub, add_viewed


# Anime

@login_required
def anime_list(request):
    animes = Anime.objects
    for word in request.GET.get('anime', '').split():
        animes = animes.filter(name__icontains=word)
    return render(request, 'ergoanimes/anime_list.html', {
        'animes': AnimeTable(data=animes.all(), data_extra={'user': request.user}),
    })


@login_required
def anime_byseason(request):
    animes_byseason = defaultdict(list)
    for anime in Anime.objects.filter(season_start__isnull=False):
        animes_byseason[anime.season_start].append(anime)
    return render(request, 'ergoanimes/useranime_status.html', {
        'tables': [('', i.strftime('%B/%Y'), AnimeTable(data=animes_byseason[i], data_extra={'user': request.user})) for i in sorted(animes_byseason, reverse=True)],
    })


@login_required
def anime_show(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    try:
        useranime = anime.useranimes.get(user=request.user)
    except ObjectDoesNotExist:
        useranime = None
    return render(request, 'ergoanimes/anime_show.html', {
        'anime': anime,
        'useranime': useranime,
    })


@login_required
def anime_form(request, pk=None):
    if pk:
        if not request.user.has_perm('ergoanimes.change_anime'):
            return redirect_to_login(request.path)
        anime = get_object_or_404(Anime, pk=pk)
    else:
        if not request.user.has_perm('ergoanimes.add_anime'):
            return redirect_to_login(request.path)
        anime = None
    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES, instance=anime)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Anime "%(name)s" saved') % {'name': form.instance.name})
            return redirect(form.instance)
    else:
        form = AnimeForm(instance=anime)
    return render(request, 'ergoanimes/anime_form.html', {
        'form': form,
        'anime': anime,
    })


class AnimeDeleteView(DeleteView):
    model = Anime
    template = 'ergoanimes/base.html'
    message = _('Delete anime "%(title)s"?')
    message_deleted = _('Anime "%(title)s" deleted')
    redirect = 'ergoanimes:anime_list'

    def title(self, anime):
        return anime.name

    def make_filter(self, request, pk):
        return {'pk': pk}


anime_delete = permission_required('ergoanimes.delete_anime')(
    AnimeDeleteView.as_view()
)


# Fansub

@login_required
def fansub_list(request):
    return render(request, 'ergoanimes/fansub_list.html', {
        'fansubs': FansubTable(data=Fansub.objects.all(), data_extra={'user': request.user}),
    })


@login_required
def fansub_show(request, pk):
    fansub = get_object_or_404(Fansub, pk=pk)
    return render(request, 'ergoanimes/fansub_show.html', {
        'fansub': fansub,
    })


@login_required
def fansub_form(request, pk=None):
    if pk:
        if not request.user.has_perm('ergoanimes.change_fansub'):
            return redirect_to_login(request.path)
        fansub = get_object_or_404(Fansub, pk=pk)
    else:
        if not request.user.has_perm('ergoanimes.add_fansub'):
            return redirect_to_login(request.path)
        fansub = None
    if request.method == 'POST':
        form = FansubForm(request.POST, request.FILES, instance=fansub)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Fansub "%(name)s" saved') % {'name': form.instance.name})
            return redirect(form.instance)
    else:
        form = FansubForm(instance=fansub)
    return render(request, 'ergoanimes/fansub_form.html', {
        'form': form,
        'fansub': fansub,
    })


class FansubDeleteView(DeleteView):
    model = Fansub
    template = 'ergoanimes/base.html'
    message = _('Delete fansub "%(title)s"?')
    message_deleted = _('Fansub "%(title)s" deleted')
    redirect = 'ergoanimes:fansub_list'

    def title(self, fansub):
        return fansub.name

    def make_filter(self, request, pk):
        return {'pk': pk}


fansub_delete = permission_required('ergoanimes.delete_fansub')(
    FansubDeleteView.as_view()
)


# Genre

@login_required
def genre_list(request):
    return render(request, 'ergoanimes/genre_list.html', {
        'genres': GenreTable(data=sorted(Genre.objects.all(), key=lambda x: x.get_genre_display()),
                             data_extra={'user': request.user}),
    })


@login_required
def genre_show(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    return render(request, 'ergoanimes/genre_show.html', {
        'genre': genre,
    })


# User Anime

@login_required
def useranime_list(request):
    return render(request, 'ergoanimes/useranime_list.html', {
        'useranimes': UserAnimeTable(data=UserAnime.objects.filter(user=request.user)),
    })


@login_required
def useranime_status(request):
    useranimes = UserAnime.objects.filter(user=request.user)
    status = list(CHOICES_STATUS)
    status.append(status.pop(0))
    return render(request, 'ergoanimes/useranime_status.html', {
        'tables': [(s[0], s[1], UserAnimeStatusTable(data=useranimes.filter(status=s[0]))) for s in status],
    })


@login_required
def useranime_reports(request):
    return render(request, 'ergoanimes/useranime_status.html', {
        'tables': (
            ('watch', _('Watch'), UserAnimeTable(data=reports.watch(request.user))),
            ('down', _('Down'), UserAnimeDownTable(data=reports.down(request.user))),
            ('new-watch', _('New for Watch'), UserAnimeTable(data=reports.new_watch(request.user))),
            ('new-down', _('New for Down'), UserAnimeDownTable(data=reports.new_down(request.user))),
        ),
    })


@login_required
def useranime_check(request):
    return render(request, 'ergoanimes/useranime_list.html', {
        'useranimes': UserAnimePubTable(data=reports.check_new(request.user)),
    })


@login_required
def useranime_bynote(request):
    useranimes = UserAnimeTable(data=UserAnime.objects.filter(user=request.user, note__isnull=False)
                                .order_by('-note', 'anime__name'))
    return render(request, 'ergoanimes/useranime_list.html', {
        'useranimes': useranimes,
    })


@login_required
def useranime_viewedhd(request):
    return render(request, 'ergoanimes/useranime_list.html', {
        'useranimes': UserAnimeStatusTable(data=reports.viewed_hd(request.user)),
    })


@login_required
def useranime_form(request, pk):
    anime = Anime.objects.get(pk=pk)
    try:
        useranime = anime.useranimes.get(user=request.user)
    except ObjectDoesNotExist:
        useranime = UserAnime(anime=anime)
    if request.method == 'POST':
        form = UserAnimeForm(request.POST, instance=useranime)
        if form.is_valid():
            instance = form.instance
            instance.user = request.user
            instance.anime = anime
            instance.save()
            messages.add_message(request, messages.INFO, _('Anime "%(name)s" update in list') % {'name': anime.name})
            return redirect(anime)
    else:
        form = UserAnimeForm(instance=useranime)
    return render(request, 'ergoanimes/useranime_form.html', {
        'form': form,
        'anime': anime,
        'useranime': useranime,
    })


class UserAnimeDeleteView(DeleteView):
    model = UserAnime
    template = 'ergoanimes/base.html'
    message = _('Remove anime "%(title)s" from list?')
    message_deleted = _('Anime "%(title)s" removed')
    redirect = 'ergoanimes:anime'

    def title(self, useranime):
        return useranime.anime.name

    def make_filter(self, request, pk):
        return {'user': request.user, 'anime': pk}

    def redirect_args(self, request, pk):
        return (pk,)


useranime_delete = UserAnimeDeleteView.as_view()


@login_required
def useranime_plus(request, pk, episode_type):
    useranime = get_object_or_404(UserAnime, user=request.user, anime__pk=pk)
    try:
        if episode_type == 'pub':
            add_pub(useranime)
        elif episode_type == 'down':
            add_down(useranime)
        elif episode_type == 'viewed':
            add_viewed(useranime)
        else:
            return HttpResponse(_('Episode type not identify'), status=406)
        useranime.clean()
        useranime.save()
        if 'HTTP_REFERER' in request.META:
            return redirect(request.META['HTTP_REFERER'])
        return HttpResponse(status=204)
    except ValidationError as e:
        return HttpResponse('\n'.join(e.messages), status=406)
