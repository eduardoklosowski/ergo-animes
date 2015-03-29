# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ErgoAnimesConfig(AppConfig):
    name = 'ergoanimes'
    verbose_name = _('Ergo Animes')
    ergo_url = 'animes'
    ergo_url_index = 'ergoanimes:index'
    ergo_verbose_name = _('Animes')
