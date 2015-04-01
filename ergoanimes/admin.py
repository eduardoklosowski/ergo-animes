# -*- coding: utf-8 -*-

from __future__ import unicode_literals

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
    list_display = ('name', 'media_type', 'has_img', 'episodes', 'season_start', 'get_genres_display', 'mal', 'anidb',
                    'has_synopsis')
    list_filter = ('media_type', 'episodes', 'genres')
    search_fields = ('name', '=mal', '=anidb')


@admin.register(models.Fansub)
class FansubAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'irc', 'has_img', 'active')
    list_filter = ('active',)
    search_fields = ('name',)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre',)


@admin.register(models.UserAnime)
class UserAnimeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_start'
    fields = (('user', 'anime'),
              'status',
              'fansub',
              ('quality', 'resolution'),
              ('episodes_pub', 'episodes_down', 'episodes_viewed', 'times'),
              ('date_start', 'date_end'),
              'link',
              'note',
              'comment')
    list_display = ('user', 'anime', 'status', 'fansub', 'quality', 'note')
    list_display_links = ('user', 'anime')
    list_filter = ('status', 'quality')
    search_fields = ('=user__username', 'anime__name', '=anime__mal', '=anime__anidb')
