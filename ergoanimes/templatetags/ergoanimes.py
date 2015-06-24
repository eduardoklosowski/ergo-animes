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

from django import template
from django.core.urlresolvers import reverse

from ..models import CHOICES_STATUS


register = template.Library()

STATUS = dict(CHOICES_STATUS)


# Filters

@register.filter
def ergoanimes_getcount(obj, count):
    return count.get(obj.pk, 0)


@register.filter
def ergoanimes_getstatus(anime, anime_status):
    return STATUS.get(anime_status.get(anime.pk, None), '-')


# Tags

@register.simple_tag
def ergoanimes_episodes(episodes_a, episodes_b):
    if episodes_a is None:
        episodes_a = '-'
    if episodes_b is None:
        episodes_b = '-'
    return '%s/%s' % (episodes_a, episodes_b)


@register.simple_tag
def ergoanimes_menustatus():
    url = reverse('ergoanimes:useranime_statuslist')
    item = '<li><a href="%s#%s">%s</a></li>'
    return ''.join(item % (url, status_id, status) for status_id, status in CHOICES_STATUS[1:] + CHOICES_STATUS[:1])
