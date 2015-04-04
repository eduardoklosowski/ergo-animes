# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import date


def add_down(useranime):
    if useranime.episodes_down is None:
        useranime.episodes_down = 0
    useranime.episodes_down += 1


def add_pub(useranime):
    if useranime.episodes_pub is None:
        useranime.episodes_pub = 0
    useranime.episodes_pub += 1


def add_viewed(useranime):
    if useranime.episodes_viewed is None:
        useranime.episodes_viewed = 0
    useranime.episodes_viewed += 1
    if useranime.episodes_viewed == 1 and useranime.status in ('new', 'watching', 'hold'):
        useranime.status = 'watching'
        if not useranime.date_start:
            useranime.date_start = date.today()
    if useranime.anime.episodes and useranime.episodes_viewed == useranime.anime.episodes:
        useranime.status = 'completed'
        useranime.times += 1
        if not useranime.date_end:
            useranime.date_end = date.today()


def calc_season_end(air_date):
    if not air_date:
        return None

    year = air_date.year
    month = air_date.month
    day = air_date.day

    if month == 1 and day < 15:
        return date(year - 1, 10, 1)
    if month < 4 or (month == 4 and day < 15):
        return date(year, 1, 1)
    if month < 7 or (month == 7 and day < 15):
        return date(year, 4, 1)
    if month < 10 or (month == 10 and day < 15):
        return date(year, 7, 1)
    return date(year, 10, 1)


def calc_season_start(air_date):
    if not air_date:
        return None

    year = air_date.year
    month = air_date.month
    day = air_date.day

    if month == 12 and day > 15:
        return date(year + 1, 1, 1)
    if month > 9 or (month == 9 and day > 15):
        return date(year, 10, 1)
    if month > 6 or (month == 6 and day > 15):
        return date(year, 7, 1)
    if month > 3 or (month == 3 and day > 15):
        return date(year, 4, 1)
    return date(year, 1, 1)
