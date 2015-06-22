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

from django.conf import settings
from django.core.management.base import BaseCommand
import os

from ...models import Anime


class Command(BaseCommand):
    help = 'Lista imagens velhas de animes'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--delete', dest='delete', action='store_true', default=False,
                            help='Remove as imagens')

    def handle(self, *args, **options):
        prefix = Anime._meta.get_field('img').upload_to
        if prefix.endswith('/'):
            prefix = prefix[:-1]
        directory = os.path.join(settings.MEDIA_ROOT, prefix)

        images_directory = set(os.listdir(directory))

        images_saved = Anime.objects.filter(img__startswith=prefix).values_list('img', flat=True)
        images_saved = set(img[len(prefix) + 1:] for img in images_saved)

        images_delete = images_directory - images_saved
        for image in images_delete:
            self.stdout.write('%s\n' % os.path.join(prefix, image))
            if options['delete']:
                os.unlink(os.path.join(directory, image))
