# -*- coding: utf-8 -*-

import os

from ergo.settings.dev import *  # NOQA


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS += (
    'ergoanimes',
)

DATABASES['default']['NAME'] = os.path.join(BASE_DIR, 'db.sqlite3')

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
