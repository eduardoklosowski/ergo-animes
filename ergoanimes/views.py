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

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from ergo.views import LoginRequiredMixin, PermissionRequiredMixin

from . import models


# Fansub

class FansubListView(LoginRequiredMixin, generic.ListView):
    model = models.Fansub


class FansubDetailView(LoginRequiredMixin, generic.DetailView):
    model = models.Fansub


class FansubCreateView(PermissionRequiredMixin, generic.CreateView):
    permission = 'ergoanimes.add_fansub'
    model = models.Fansub
    fields = ('name', 'site', 'irc', 'active', 'img')


class FansubUpdateView(PermissionRequiredMixin, generic.UpdateView):
    permission = 'ergoanimes.change_fansub'
    model = models.Fansub
    fields = ('name', 'site', 'irc', 'active', 'img')


class FansubDeleteView(PermissionRequiredMixin, generic.DeleteView):
    permission = 'ergoanimes.delete_fansub'
    model = models.Fansub
    success_url = reverse_lazy('ergoanimes:fansub_list')
