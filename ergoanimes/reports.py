# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import F, Q

from . import models


def check_new(user):
    return models.UserAnime.objects.filter(user=user)\
        .exclude(status__in=('completed', 'drop'))\
        .exclude(anime__episodes=F('episodes_pub'))\
        .filter(Q(status='watching') | (~Q(status='watching') & Q(episodes_down__isnull=False)))


def down(user):
    return models.UserAnime.objects.filter(user=user)\
        .exclude(status__in=('completed', 'drop'))\
        .filter(Q(status='watching') | (~Q(status='watching') & Q(episodes_down__isnull=False)))\
        .filter(episodes_down__lt=F('episodes_pub'))


def new_down(user):
    return models.UserAnime.objects.filter(user=user)\
        .filter(status='new', episodes_pub=F('anime__episodes'))


def new_watch(user):
    return models.UserAnime.objects.filter(user=user)\
        .filter(status='new', episodes_down=F('anime__episodes'))


def watch(user):
    return models.UserAnime.objects.filter(user=user)\
        .filter(status__in=('watching', 'hold'), episodes_viewed__lt=F('episodes_down'))
