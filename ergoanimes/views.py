# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .forms import AnimeForm, FansubForm, UserAnimeForm
from .models import Anime, Fansub, Genre, UserAnime
from .tables import AnimeTable, FansubTable, GenreTable, UserAnimeTable


# Anime

@login_required
def anime_list(request):
    return render(request, 'ergoanimes/anime_list.html', {
        'animes': AnimeTable(data=Anime.objects.all()),
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


@login_required
@permission_required('ergoanimes.delete_anime')
def anime_delete(request, pk):
    anime = get_object_or_404(Anime, pk=pk)
    if request.GET.get('confirm', '') == 'y':
        anime.delete()
        messages.add_message(request, messages.INFO, _('Anime "%(name)s" deleted') % {'name': anime.name})
        return redirect('ergoanimes:fansub_list')
    return render(request, 'ergoanimes/pag_delete.html', {
        'title': _('Delete anime "%(name)s"?') % {'name': anime.name}
    })


# Fansub

@login_required
def fansub_list(request):
    return render(request, 'ergoanimes/fansub_list.html', {
        'fansubs': FansubTable(data=Fansub.objects.all()),
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


@login_required
@permission_required('ergoanimes.delete_fansub')
def fansub_delete(request, pk):
    fansub = get_object_or_404(Fansub, pk=pk)
    if request.GET.get('confirm', '') == 'y':
        fansub.delete()
        messages.add_message(request, messages.INFO, _('Fansub "%(name)s" deleted') % {'name': fansub.name})
        return redirect('ergoanimes:fansub_list')
    return render(request, 'ergoanimes/pag_delete.html', {
        'title': _('Delete fansub "%(name)s"?') % {'name': fansub.name}
    })


# Genre

@login_required
def genre_list(request):
    return render(request, 'ergoanimes/genre_list.html', {
        'genres': GenreTable(data=Genre.objects.all()),
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


@login_required
def useranime_delete(request, pk):
    useranime = get_object_or_404(UserAnime, user=request.user, anime=pk)
    if request.GET.get('confirm', '') == 'y':
        useranime.delete()
        messages.add_message(request, messages.INFO,
                             _('Anime "%(name)s" list removed') % {'name': useranime.anime.name})
        return redirect(useranime.anime)
    return render(request, 'ergoanimes/pag_delete.html', {
        'title': _('Remove anime "%(name)s" from list?') % {'name': useranime.anime.name},
    })
