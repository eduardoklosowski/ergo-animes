# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class GenreTable(Table):
    columns = ({'name': _('Genre'),
                'value': lambda x: x.get_linkdisplay()},)
