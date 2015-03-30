# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .utils import calc_season_end, calc_season_start
from .validators import check_irc


CHOICES_GENRES = (
    (1, _('Action')),
    (2, _('Adventure')),
    (3, _('Cars')),
    (4, _('Comedy')),
    (5, _('Dementia')),
    (6, _('Demons')),
    (7, _('Drama')),
    (8, _('Ecchi')),
    (9, _('Fantasy')),
    (10, _('Game')),
    (11, _('Harem')),
    (12, _('Hentai')),
    (13, _('Historical')),
    (14, _('Horror')),
    (15, _('Josei')),
    (16, _('Kids')),
    (17, _('Magic')),
    (18, _('Martial Arts')),
    (19, _('Mecha')),
    (20, _('Military')),
    (21, _('Music')),
    (22, _('Mystery')),
    (23, _('Parody')),
    (24, _('Police')),
    (25, _('Psychological')),
    (26, _('Romance')),
    (27, _('Samurai')),
    (28, _('School')),
    (29, _('Sci-Fi')),
    (30, _('Seinen')),
    (31, _('Shoujo')),
    (32, _('Shoujo Ai')),
    (33, _('Shounen')),
    (34, _('Shounen Ai')),
    (35, _('Slice of Life')),
    (36, _('Space')),
    (37, _('Sports')),
    (38, _('Super Power')),
    (39, _('Supernatural')),
    (40, _('Thriller')),
    (41, _('Vampire')),
    (42, _('Yaoi')),
    (43, _('Yuri')),
)

CHOICES_MEDIA_TYPE = (
    ('', '-'),
    ('tv', _('TV')),
    ('special', _('Special')),
    ('ova', _('OVA')),
    ('movie', _('Movie')),
    ('ona', _('ONA')),
)


def sorted_choices_genres():
    for genre in sorted(CHOICES_GENRES, key=lambda x: x[1]):
        yield genre


@python_2_unicode_compatible
class Anime(models.Model):
    name = models.CharField(_('name'), max_length=200, unique=True)
    media_type = models.CharField(_('type'), max_length=8, default='', choices=CHOICES_MEDIA_TYPE)
    img = models.ImageField(_('image'), upload_to='ergoanimes/anime', blank=True, null=True)
    episodes = models.PositiveSmallIntegerField(_('episodes'), blank=True, null=True)
    duration = models.PositiveSmallIntegerField(_('duration'), blank=True, null=True)
    air_start = models.DateField(_('start air'), blank=True, null=True)
    air_end = models.DateField(_('end air'), blank=True, null=True)
    season_start = models.DateField(_('start season'), blank=True, null=True)
    season_end = models.DateField(_('end season'), blank=True, null=True)
    genres = models.ManyToManyField('Genre', verbose_name=_('genres'), related_name='animes', blank=True)
    mal = models.PositiveIntegerField(_('MyAnimeList ID'), blank=True, null=True, unique=True)
    anidb = models.PositiveIntegerField(_('AniDB ID'), blank=True, null=True, unique=True)
    synopsis = models.TextField(_('synopsis'), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('anime')
        verbose_name_plural = _('animes')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ergoanimes:anime', args=(self.pk,))

    def clean(self):
        self.calc_season()

    def calc_season(self):
        if not self.season_start:
            self.season_start = calc_season_start(self.air_start)
        if not self.season_end:
            self.season_end = calc_season_end(self.air_end)

    def get_linkdisplay(self):
        return mark_safe('<a href="%s">%s</a>' % (self.get_absolute_url(), self.name))

    def has_img(self):
        return self.img != ''
    has_img.boolean = True
    has_img.short_description = _('Has image?')

    def get_episodes_display(self):
        if self.episodes is not None:
            return self.episodes
        return '-'

    def get_season_start_display(self):
        if self.season_start is not None:
            return self.season_start.strftime('%b/%Y')
        return '-'

    def get_genres_display(self):
        genres = self.genres.all()
        if genres:
            return ', '.join([str(genre) for genre in sorted(genres, key=lambda x: x.get_genre_display())])
        return '-'
    get_genres_display.short_description = _('genres')

    def get_genres_linkdisplay(self):
        genres = self.genres.all()
        if genres:
            return mark_safe(', '.join(['<a href="%s">%s</a>' % (genre.get_absolute_url(), genre)
                                        for genre in sorted(self.genres.all(), key=lambda x: x.get_genre_display())]))
        return '-'

    def get_links_linkdisplay(self):
        links = (('MAL', self.get_mal_link()),
                 ('AniDB', self.get_anidb_link()))
        links = [link for link in links if link[1]]
        if links:
            return mark_safe(' '.join(['<a href="%s" target="_blank">%s</a>' % (link[1], link[0]) for link in links]))
        return '-'

    def get_mal_link(self):
        if self.mal:
            return 'http://myanimelist.net/anime/%d/' % self.mal
        return None

    def get_anidb_link(self):
        if self.anidb:
            return 'http://anidb.net/perl-bin/animedb.pl?show=anime&aid=%d' % self.anidb
        return None

    def has_synopsis(self):
        return self.synopsis != ''
    has_synopsis.boolean = True
    has_synopsis.short_description = _('Has synopsis?')


@python_2_unicode_compatible
class Fansub(models.Model):
    name = models.CharField(_('name'), max_length=40, unique=True)
    site = models.URLField(_('site'), blank=True)
    irc = models.CharField(_('IRC'), max_length=200, blank=True, validators=[check_irc])
    active = models.BooleanField(_('active'), blank=True, default=True)
    img = models.ImageField(_('image'), upload_to='ergoanimes/fansub', blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('fansub')
        verbose_name_plural = _('fansubs')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ergoanimes:fansub', args=(self.pk,))

    def get_linkdisplay(self):
        return mark_safe('<a href="%s">%s</a>' % (self.get_absolute_url(), self.name))

    def get_site_linkdisplay(self):
        if self.site:
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (
                self.site,
                self.site,
            ))
        return '-'

    def get_irc_linkdisplay(self):
        if self.irc:
            return mark_safe('<a href="%s" target="_blank">%s</a>' % (
                self.irc,
                self.irc,
            ))
        return '-'

    def get_active_display(self):
        if self.active:
            return _('Yes')
        return _('No')

    def has_img(self):
        return self.img != ''
    has_img.boolean = True
    has_img.short_description = _('has image?')


@python_2_unicode_compatible
class Genre(models.Model):
    genre = models.PositiveSmallIntegerField(_('genre'), primary_key=True, choices=sorted_choices_genres())

    class Meta:
        ordering = ('genre',)
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.get_genre_display()

    def get_absolute_url(self):
        return reverse('ergoanimes:genre', args=(self.pk,))

    def get_linkdisplay(self):
        return mark_safe('<a href="%s">%s</a>' % (self.get_absolute_url(), self.get_genre_display()))

    def count_animes(self):
        return self.animes.count()
