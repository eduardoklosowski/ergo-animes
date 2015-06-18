# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import F, Manager, Q


class UserAnimeManager(Manager):
    def check_new(self, user):
        return self.filter(user=user).exclude(
            status__in=('complated', 'drop'),
        ).filter(
            Q(status='watching') | Q(episodes_down__isnull=False),
            episodes_pub__lt=F('anime__episodes'),
        ).select_related('anime')

    def down(self, user):
        return self.filter(user=user).exclude(
            status__in=('completed', 'drop'),
        ).filter(
            Q(status='watching') | Q(episodes_down__isnull=False),
            episodes_down__lt=F('episodes_pub'),
        ).select_related('anime')

    def new_down(self, user):
        return self.filter(user=user).filter(
            status='new',
        ).filter(
            Q(episodes_down__isnull=True) | ~Q(episodes_down=F('episodes_pub')),
            episodes_pub=F('anime__episodes'),
        ).select_related('anime')

    def new_watch(self, user):
        return self.filter(user=user).filter(
            status='new',
            episodes_down=F('anime__episodes'),
        ).select_related('anime')

    def watch(self, user):
        return self.filter(user=user).filter(
            status__in=('watching', 'hold'),
            episodes_viewed__lt=F('episodes_down'),
        ).select_related('anime')
