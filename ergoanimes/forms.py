# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from ergo.foundation.forms import FoundationForm

from . import models


class FansubForm(forms.ModelForm, FoundationForm):
    class Meta:
        fields = ('name', 'site', 'irc', 'img', 'active')
        model = models.Fansub

        foundation_column_class = {
            'name': 'small-12',
        }
        foundation_fieldsets = (
            (None, ('name',)),
            (None, ('site', 'irc')),
            (None, ('img', 'active')),
        )
