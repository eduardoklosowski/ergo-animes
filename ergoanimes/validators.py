# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def check_irc(value):
    if not value.startswith('irc://'):
        raise ValidationError(_('The address should begin with irc://'))
