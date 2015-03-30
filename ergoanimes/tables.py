# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class FansubTable(Table):
    columns = ({'name': _('Fansub'),
                'value': lambda x: x.get_linkdisplay()},
               {'name': _('Site'),
                'class': 'show-for-medium-up',
                'value': lambda x: x.get_site_linkdisplay()},
               {'name': _('IRC'),
                'class': 'show-for-large-up',
                'value': lambda x: x.get_irc_linkdisplay()},
               {'name': _('Active'),
                'header_class': 'width-6r',
                'value': lambda x: x.get_active_display()})


class GenreTable(Table):
    columns = ({'name': _('Genre'),
                'value': lambda x: x.get_linkdisplay()},)
