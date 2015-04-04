# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from . import reports


class ErgoAnimesConfig(AppConfig):
    name = 'ergoanimes'
    verbose_name = _('Ergo Animes')
    ergo_url = 'animes'
    ergo_url_index = 'ergoanimes:index'
    ergo_verbose_name = _('Animes')

    def ergo_notifications(self, request):
        html = []
        reports_url = reverse('ergoanimes:useranime_reports')
        animes_status = (
            ('watch', _('Watch'), reports.watch(request.user)),
            ('down', _('Down'), reports.down(request.user)),
        )
        for id_status, status, useranimes in animes_status:
            count = useranimes.count()
            if not count:
                continue
            text = ['<ul class="no-bullet no-margin">']
            for useranime in useranimes:
                if id_status == 'watch':
                    episodes = '[%s]' % useranime.get_episodes_viewed_display()
                elif id_status == 'down':
                    episodes = '[%s]' % useranime.get_episodes_down_display()
                text.append('<li>%s %s</li>' % (useranime.anime.get_linkdisplay(), episodes))
            text.append('</ul>')
            html.append({'url': '%s#%s' % (reports_url, id_status),
                         'title': '%s: %s' % (self.ergo_verbose_name, status),
                         'count': count,
                         'text': mark_safe(''.join(text))})
        return html
