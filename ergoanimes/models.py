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

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe


# Choices

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


# Models

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
        return ''
