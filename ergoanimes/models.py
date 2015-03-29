# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


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


def sorted_choices_genres():
    for genre in sorted(CHOICES_GENRES, key=lambda x: x[1]):
        yield genre


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
