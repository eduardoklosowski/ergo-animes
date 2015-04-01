# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from ergo.foundation.forms import FoundationForm

from . import models


class AnimeForm(forms.ModelForm, FoundationForm):
    class Meta:
        fields = ('name', 'media_type', 'episodes', 'duration', 'img', 'air_start', 'air_end', 'season_start',
                  'season_end', 'genres', 'mal', 'anidb', 'synopsis')
        model = models.Anime

        foundation_column_class = {
            'name': 'small-12',
            'media_type': 'small-12 medium-4',
            'episodes': 'small-12 medium-4',
            'duration': 'small-12 medium-4',
            'img': 'small-12',
            'genres': 'small-12',
            'synopsis': 'small-12',
        }
        foundation_fieldsets = (
            (None, ('name', 'media_type', 'episodes', 'duration', 'img')),
            (_('Dates'), ('air_start', 'air_end', 'season_start', 'season_end')),
            (None, ('genres', 'mal', 'anidb', 'synopsis')),
        )


class FansubForm(forms.ModelForm, FoundationForm):
    class Meta:
        fields = ('name', 'site', 'irc', 'img', 'active')
        model = models.Fansub

        foundation_column_class = {
            'name': 'small-12',
        }
        foundation_fieldsets = (
            (None, ('name',)),
            (None, ('site', 'irc')),
            (None, ('img', 'active')),
        )


class UserAnimeForm(forms.ModelForm, FoundationForm):
    class Meta:
        fields = ('status', 'fansub', 'quality', 'resolution', 'episodes_pub', 'episodes_down', 'episodes_viewed',
                  'times', 'date_start', 'date_end', 'link', 'note', 'comment')
        model = models.UserAnime

        foundation_column_class = {
            'comment': 'small-12',
        }
        foundation_fieldsets = (
            (None, ('status', 'fansub')),
            (None, ('quality', 'resolution')),
            (_('Episodes'), ('episodes_pub', 'episodes_down', 'episodes_viewed', 'times')),
            (_('Date'), ('date_start', 'date_end')),
            (None, ('link', 'note')),
            (None, ('comment',)),
        )
