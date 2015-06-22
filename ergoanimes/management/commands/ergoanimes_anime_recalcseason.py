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

from django.core.management.base import BaseCommand
from django.utils.six.moves import input

from ...models import Anime, calc_season_start, calc_season_end


class Command(BaseCommand):
    help = 'Recalcula período da temporada'

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start', dest='end', action='store_false', default=True,
                            help='Calcula apenas data de início')
        parser.add_argument('-e', '--end', dest='start', action='store_false', default=True,
                            help='Calcula apenas data de termino')

    def handle(self, *args, **options):
        if options['start']:
            for anime in Anime.objects.exclude(air_start__isnull=True):
                recalc_start = calc_season_start(anime.air_start)
                if anime.season_start != recalc_start:
                    self.stdout.write('%s [%s]\n  Data de início de %s para %s: (y/N)' %
                                      (anime, anime.air_start, anime.season_start, recalc_start))
                    if input().lower() == 'y':
                        anime.season_start = recalc_start
                        anime.save()

        if options['end']:
            for anime in Anime.objects.exclude(air_end__isnull=True):
                recalc_end = calc_season_end(anime.air_end)
                if anime.season_end != recalc_end and recalc_end >= anime.season_start:
                    self.stdout.write('%s [%s]\n  Data de termino de %s para %s: (y/N)' %
                                      (anime, anime.air_end, anime.season_end, recalc_end))
                    if input().lower() == 'y':
                        anime.season_end = recalc_end
                        anime.save()
