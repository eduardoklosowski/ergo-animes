# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class AnimeTable(Table):
    columns = ({'name': _('Anime'),
                'value': lambda x: x.get_linkdisplay()},
               {'name': _('Type'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_media_type_display()},
               {'name': _('Episodes'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_episodes_display()},
               {'name': _('Season'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_season_start_display()},
               {'name': _('Genres'),
                'class': 'show-for-large-up',
                'value': lambda x: x.get_genres_linkdisplay()},
               {'name': _('Links'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_links_linkdisplay()})


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
                'value': lambda x: x.get_linkdisplay()},
               {'name': _('Animes'),
                'header_class': 'width-6r',
                'value': lambda x: x.count_animes()})


class UserAnimeTable(Table):
    columns = ({'name': _('Anime'),
                'value': lambda x: x.anime.get_linkdisplay()},
               {'name': _('Type'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.anime.get_media_type_display()},
               {'name': _('Season'),
                'class': 'show-for-large-up',
                'header_class': 'width-6r',
                'value': lambda x: x.anime.get_season_start_display()},
               {'name': _('Note'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_note_display()},
               {'name': _('Episodes'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.anime.get_episodes_display()},
               {'name': _('Status'),
                'header_class': 'width-6r',
                'value': lambda x: x.get_status_display()},
               {'name': _('Fansub'),
                'class': 'show-for-large-up',
                'value': lambda x: x.get_fansub_linkdisplay()},
               {'name': _('Link'),
                'class': 'show-for-large-up',
                'value': lambda x: x.get_link_linkdisplay()})
