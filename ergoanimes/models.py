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

from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import date as datefilter
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe


# Choices

CHOICES_MEDIA_TYPE = (
    ('', '-'),
    ('tv', 'TV'),
    ('special', 'Especial'),
    ('ova', 'OVA'),
    ('movie', 'Filme'),
    ('ona', 'ONA'),
)


def get_genres():
    genres = (
        (1, 'Ação'),
        (2, 'Aventura'),
        (3, 'Carros'),
        (4, 'Comédia'),
        (5, 'Demencia'),
        (6, 'Demônio'),
        (7, 'Drama'),
        (8, 'Ecchi'),
        (9, 'Fantasia'),
        (10, 'Jogo'),
        (11, 'Harém'),
        (12, 'Hentai'),
        (13, 'Histórico'),
        (14, 'Horror'),
        (15, 'Josei'),
        (16, 'Crianças'),
        (17, 'Mágica'),
        (18, 'Artes Marciais'),
        (19, 'Mecha'),
        (20, 'Militar'),
        (21, 'Música'),
        (22, 'Mistério'),
        (23, 'Paródia'),
        (24, 'Policial'),
        (25, 'Psicológico'),
        (26, 'Romance'),
        (27, 'Samurai'),
        (28, 'Escola'),
        (29, 'Sci-Fi'),
        (30, 'Seinen'),
        (31, 'Shoujo'),
        (32, 'Shoujo Ai'),
        (33, 'Shounen'),
        (34, 'Shounen Ai'),
        (35, 'Slice of Life'),
        (36, 'Espacial'),
        (37, 'Esporte'),
        (38, 'Super Poder'),
        (39, 'Sobrenatural'),
        (40, 'Suspense'),
        (41, 'Vampiro'),
        (42, 'Yaoi'),
        (43, 'Yuri'),
    )
    return sorted(genres, key=lambda x: x[1])


# Check

def check_irc(value):
    if not value.startswith('irc://'):
        raise ValidationError('O endereço deve começar com "irc://"')


# Calc

def calc_season_end(air_date):
    if not air_date:
        return None

    air_date -= timedelta(days=21)
    year = air_date.year
    month = air_date.month

    if month >= 10:
        month = 10
    elif month >= 7:
        month = 7
    elif month >= 4:
        month = 4
    else:
        month = 1
    return date(year, month, 1)


def calc_season_start(air_date):
    if not air_date:
        return None

    air_date += timedelta(days=21)
    year = air_date.year
    month = air_date.month

    if month < 4:
        month = 1
    elif month < 7:
        month = 4
    elif month < 10:
        month = 7
    else:
        month = 10
    return date(year, month, 1)


# Models

@python_2_unicode_compatible
class Anime(models.Model):
    name = models.CharField('nome', max_length=256, unique=True)
    media_type = models.CharField('tipo', max_length=8, default='', choices=CHOICES_MEDIA_TYPE)
    img = models.ImageField('imagem', upload_to='ergoanimes/anime', blank=True, null=True)
    episodes = models.PositiveSmallIntegerField('episódios', blank=True, null=True)
    duration = models.PositiveSmallIntegerField('duração', blank=True, null=True)
    air_start = models.DateField('transmitido de', blank=True, null=True)
    air_end = models.DateField('transmitido até', blank=True, null=True)
    season_start = models.DateField('temporada de', blank=True, null=True)
    season_end = models.DateField('temporada até', blank=True, null=True)
    genres = models.ManyToManyField('Genre', verbose_name='gêneros', related_name='animes', blank=True)
    mal = models.PositiveIntegerField('MyAnimeList ID', blank=True, null=True, unique=True)
    anidb = models.PositiveIntegerField('AniDB ID', blank=True, null=True, unique=True)
    synopsis = models.TextField('sinopse', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'anime'
        verbose_name_plural = 'animes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return ''

    def clean(self):
        self.calc_season()

        if self.air_start and self.air_end and self.air_end < self.air_start:
            raise ValidationError('Data de termino antes que a de início')
        if self.season_start and self.season_end and self.season_end < self.season_start:
            raise ValidationError('Temporada de termino antes que a de início')

    def calc_season(self):
        if not self.season_start:
            self.season_start = calc_season_start(self.air_start)
        if not self.season_end:
            self.season_end = calc_season_end(self.air_end)
            if self.season_start and self.season_end and self.season_end < self.season_start:
                self.season_end = self.season_start

    def has_img(self):
        return self.img != ''
    has_img.boolean = True
    has_img.short_description = 'Tem imagem?'

    def get_air_display(self):
        air_start = self.air_start
        air_end = self.air_end
        if air_start or air_end:
            if air_start:
                air_start = datefilter(air_start, 'SHORT_DATE_FORMAT')
            else:
                air_start = '-'
            if air_end:
                air_end = datefilter(air_end, 'SHORT_DATE_FORMAT')
            else:
                air_end = '-'
            return '%s até %s' % (air_start, air_end)
        return '-'

    def get_genres_display(self):
        genres = self.genres.all()
        if genres:
            return ', '.join(str(genre) for genre in sorted(genres, key=lambda x: x.get_genre_display()))
        return '-'
    get_genres_display.short_description = 'Gêneros'

    def get_genres_linkdisplay(self):
        genres = self.genres.all()
        if genres:
            return mark_safe(', '.join('<a href="%s">%s</a>' % (genre.get_absolute_url(), genre)
                                       for genre in sorted(self.genres.all(), key=lambda x: x.get_genre_display())))
        return '-'

    def get_links_linkdisplay(self):
        links = ((self.get_mal_link(), 'MAL'),
                 (self.get_anidb_link(), 'AniDB'))
        links = [link for link in links if link[0]]
        if links:
            return mark_safe(' '.join('<a href="%s" target="_blank">%s</a>' % link for link in links))
        return '-'

    def get_mal_link(self):
        if self.mal:
            return 'http://myanimelist.net/anime/%d/' % self.mal
        return None

    def get_anidb_link(self):
        if self.anidb:
            return 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%d' % self.anidb
        return None

    def has_synopsis(self):
        return self.synopsis != ''
    has_synopsis.boolean = True
    has_synopsis.short_description = 'Tem sinopse?'


@python_2_unicode_compatible
class Fansub(models.Model):
    name = models.CharField('nome', max_length=64, unique=True)
    site = models.URLField('site', blank=True)
    irc = models.CharField('IRC', max_length=200, blank=True, validators=[check_irc])
    active = models.BooleanField('ativo', blank=True, default=True)
    img = models.ImageField('imagem', upload_to='ergoanimes/fansub', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'fansub'
        verbose_name_plural = 'fansubs'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ergoanimes:fansub', args=(self.pk,))

    def get_site_linkdisplay(self):
        if self.site:
            return mark_safe('<a href="%s">%s</a>' % (self.site, self.site))
        return '-'

    def get_irc_linkdisplay(self):
        if self.irc:
            return mark_safe('<a href="%s">%s</a>' % (self.irc, self.irc))
        return '-'

    def get_active_display(self):
        if self.active:
            return 'Sim'
        return 'Não'

    def has_img(self):
        return self.img != ''
    has_img.boolean = True
    has_img.short_description = 'Tem imagem?'


@python_2_unicode_compatible
class Genre(models.Model):
    genre = models.PositiveSmallIntegerField('gênero', primary_key=True, choices=get_genres())

    class Meta:
        verbose_name = 'gênero'
        verbose_name_plural = 'gêneros'

    def __str__(self):
        return self.get_genre_display()

    def get_absolute_url(self):
        return reverse('ergoanimes:genre', args=(self.pk,))
