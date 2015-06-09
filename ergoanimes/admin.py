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

from django.contrib import admin

from . import models


@admin.register(models.Anime)
class AnimeAdmin(admin.ModelAdmin):
    date_hierarchy = 'season_start'
    fields = (('name', 'media_type'),
              'img',
              ('episodes', 'duration'),
              ('air_start', 'air_end'),
              ('season_start', 'season_end'),
              'genres',
              ('mal', 'anidb'),
              'synopsis')
    list_display = ('name', 'media_type', 'has_img', 'episodes', 'season_start', 'get_genres_display',
                    'mal', 'anidb', 'has_synopsis')
    list_filter = ('media_type', 'episodes', 'genres')
    search_fields = ('name', '=mal', '=anidb')


@admin.register(models.Fansub)
class FansubAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'irc', 'active', 'has_img')
    list_display_links = ('name',)
    list_filter = ('active',)
    search_fields = ('name', 'site', 'irc')


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
