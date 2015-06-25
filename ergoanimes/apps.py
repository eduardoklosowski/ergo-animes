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

from django.apps import AppConfig
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class ErgoAnimesConfig(AppConfig):
    name = 'ergoanimes'
    verbose_name = 'Ergo Animes'
    ergo_url = 'ergoanimes'
    ergo_index = 'ergoanimes:useranime_statuslist'

    def ergo_notify(self, request):
        from .templatetags.ergoanimes import ergoanimes_episodes
        UserAnime = self.get_model('UserAnime')

        html = []
        report_url = reverse('ergoanimes:useranime_reportlist')
        report_list = (
            ('watch', 'Assistir', UserAnime.objects.watch(request.user)),
            ('down', 'Baixar', UserAnime.objects.down(request.user)),
        )
        for report_id, report, useranime_list in report_list:
            count = useranime_list.count()
            if not count:
                continue
            text = ['<ul class="no-bullet no-margin">']
            for useranime in useranime_list:
                if report_id == 'watch':
                    episodes = ergoanimes_episodes(useranime.episodes_viewed, useranime.episodes_down)
                elif report_id == 'down':
                    episodes = ergoanimes_episodes(useranime.episodes_down, useranime.episodes_pub)
                text.append('<li><a href="%s">%s</a> [%s]</li>' % (useranime.get_absolute_url(), useranime, episodes))
            text.append('</ul>')
            html.append({'url': '%s#%s' % (report_url, report_id),
                         'title': 'Animes: %s' % report,
                         'count': count,
                         'text': mark_safe(''.join(text))})
        return html
