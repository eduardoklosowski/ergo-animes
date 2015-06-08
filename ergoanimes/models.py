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
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe


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
        return ''

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
