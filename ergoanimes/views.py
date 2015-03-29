# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Genre
from .tables import GenreTable


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
