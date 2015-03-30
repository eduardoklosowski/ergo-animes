# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from . import models


@admin.register(models.Fansub)
class FansubAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'irc', 'has_img', 'active')
    list_filter = ('active',)
    search_fields = ('name',)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre',)
    search_fields = ('genre',)
