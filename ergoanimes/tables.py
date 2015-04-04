# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from ergo.foundation.tables import Table


class AnimeTable(Table):
    columns = ({'name': _('Anime'),
                'row_class': 'anime',
                'value': lambda x, e: x.get_anime_img_synopsis_linkdisplay()},
               {'name': _('Type'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x, e: x.get_media_type_display()},
               {'name': _('Episodes'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'row_class': 'text-right',
                'value': lambda x, e: x.get_episodes_display()},
               {'name': _('Season'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x, e: x.get_season_start_display()},
               {'name': _('Genres'),
                'class': 'show-for-large-up',
                'value': lambda x, e: x.get_genres_linkdisplay()},
               {'name': _('Status'),
                'class': 'show-for-large-up',
                'header_class': 'width-6r',
                'value': lambda x, e: x.get_useranime_status(e['user'])},
               {'name': _('Links'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x, e: x.get_links_linkdisplay()})


class FansubTable(Table):
    columns = ({'name': _('Fansub'),
                'value': lambda x, e: x.get_linkdisplay()},
               {'name': _('Site'),
                'class': 'show-for-medium-up',
                'value': lambda x, e: x.get_site_linkdisplay()},
               {'name': _('IRC'),
                'class': 'show-for-large-up',
                'value': lambda x, e: x.get_irc_linkdisplay()},
               {'name': _('Active'),
                'header_class': 'width-6r',
                'value': lambda x, e: x.get_active_display()},
               {'name': _('My List'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'row_class': 'text-right',
                'value': lambda x, e: x.count_useranimes(e['user'])})


class GenreTable(Table):
    columns = ({'name': _('Genre'),
                'value': lambda x, e: x.get_linkdisplay()},
               {'name': _('My List'),
                'header_class': 'width-6r',
                'row_class': 'text-right',
                'value': lambda x, e: x.count_useranimes(e['user'])},
               {'name': _('Animes'),
                'header_class': 'width-6r',
                'row_class': 'text-right',
                'value': lambda x, e: x.count_animes()})


class UserAnimeTable(Table):
    columns = ({'name': _('Anime'),
                'row_class': 'anime',
                'value': lambda x: x.anime.get_anime_img_synopsis_linkdisplay()},
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
                'row_class': 'text-right',
                'value': lambda x: x.get_note_display()},
               {'name': _('Episodes'),
                'class': 'show-for-medium-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_episodes_viewed_linkdisplay()},
               {'name': _('Status'),
                'header_class': 'width-6r',
                'value': lambda x: x.get_status_display()},
               {'name': _('Fansub'),
                'class': 'show-for-large-up',
                'value': lambda x: x.get_fansub_linkdisplay()},
               {'name': _('Link'),
                'class': 'show-for-large-up',
                'header_class': 'width-6r',
                'value': lambda x: x.get_link_linkdisplay()})


class UserAnimeStatusTable(UserAnimeTable):
    def __init__(self, *args, **kwargs):
        self.columns = list(self.columns)
        self.columns.pop(5)
        super(UserAnimeStatusTable, self).__init__(*args, **kwargs)


class UserAnimeDownTable(UserAnimeTable):
    def __init__(self, *args, **kwargs):
        self.columns = list(self.columns)
        self.columns[4] = self.columns[4].copy()
        self.columns[4]['value'] = lambda x: x.get_episodes_down_linkdisplay()
        super(UserAnimeDownTable, self).__init__(*args, **kwargs)


class UserAnimePubTable(UserAnimeTable):
    def __init__(self, *args, **kwargs):
        self.columns = list(self.columns)
        self.columns[4] = self.columns[4].copy()
        self.columns[4]['value'] = lambda x: x.get_episodes_pub_linkdisplay()
        super(UserAnimePubTable, self).__init__(*args, **kwargs)
