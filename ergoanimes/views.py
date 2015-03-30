# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .forms import FansubForm
from .models import Fansub, Genre
from .tables import FansubTable, GenreTable


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
