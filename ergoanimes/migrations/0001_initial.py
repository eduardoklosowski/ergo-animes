# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ergoanimes.validators
import django.core.validators
from django.conf import settings


def insert_genres(apps, schema_editor):
    Genre = apps.get_model('ergoanimes', 'Genre')
    Genre.objects.bulk_create([Genre(genre=genre) for genre in range(1, 44)])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=200, unique=True)),
                ('media_type', models.CharField(default='', verbose_name='type', max_length=8, choices=[('', '-'), ('tv', 'TV'), ('special', 'Special'), ('ova', 'OVA'), ('movie', 'Movie'), ('ona', 'ONA')])),
                ('img', models.ImageField(blank=True, null=True, verbose_name='image', upload_to='ergoanimes/anime')),
                ('episodes', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='episodes')),
                ('duration', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='duration')),
                ('air_start', models.DateField(blank=True, null=True, verbose_name='start air')),
                ('air_end', models.DateField(blank=True, null=True, verbose_name='end air')),
                ('season_start', models.DateField(blank=True, null=True, verbose_name='start season')),
                ('season_end', models.DateField(blank=True, null=True, verbose_name='end season')),
                ('mal', models.PositiveIntegerField(blank=True, null=True, verbose_name='MyAnimeList ID', unique=True)),
                ('anidb', models.PositiveIntegerField(blank=True, null=True, verbose_name='AniDB ID', unique=True)),
                ('synopsis', models.TextField(blank=True, verbose_name='synopsis')),
            ],
            options={
                'verbose_name_plural': 'animes',
                'verbose_name': 'anime',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Fansub',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=40, unique=True)),
                ('site', models.URLField(blank=True, verbose_name='site')),
                ('irc', models.CharField(blank=True, validators=[ergoanimes.validators.check_irc], verbose_name='IRC', max_length=200)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('img', models.ImageField(blank=True, null=True, verbose_name='image', upload_to='ergoanimes/fansub')),
            ],
            options={
                'verbose_name_plural': 'fansubs',
                'verbose_name': 'fansub',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.PositiveSmallIntegerField(choices=[(1, 'Action'), (2, 'Adventure'), (3, 'Cars'), (4, 'Comedy'), (5, 'Dementia'), (6, 'Demons'), (7, 'Drama'), (8, 'Ecchi'), (9, 'Fantasy'), (10, 'Game'), (11, 'Harem'), (12, 'Hentai'), (13, 'Historical'), (14, 'Horror'), (15, 'Josei'), (16, 'Kids'), (17, 'Magic'), (18, 'Martial Arts'), (19, 'Mecha'), (20, 'Military'), (21, 'Music'), (22, 'Mystery'), (23, 'Parody'), (24, 'Police'), (25, 'Psychological'), (26, 'Romance'), (27, 'Samurai'), (28, 'School'), (29, 'Sci-Fi'), (30, 'Seinen'), (31, 'Shoujo'), (32, 'Shoujo Ai'), (33, 'Shounen'), (34, 'Shounen Ai'), (35, 'Slice of Life'), (36, 'Space'), (37, 'Sports'), (38, 'Super Power'), (39, 'Supernatural'), (40, 'Thriller'), (41, 'Vampire'), (42, 'Yaoi'), (43, 'Yuri')], verbose_name='genre', serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'genres',
                'verbose_name': 'genre',
                'ordering': ('genre',),
            },
        ),
        migrations.CreateModel(
            name='UserAnime',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.CharField(verbose_name='status', max_length=9, choices=[('new', 'New'), ('watching', 'Watching'), ('hold', 'Hold'), ('completed', 'Completed'), ('drop', 'Drop')])),
                ('quality', models.CharField(blank=True, verbose_name='quality', max_length=6, choices=[('', '-'), ('bluray', 'Blu-ray'), ('hdtv', 'HDTV'), ('dvd', 'DVD'), ('tv', 'TV'), ('web', 'Web')])),
                ('resolution', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='resolution')),
                ('episodes_pub', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='published')),
                ('episodes_down', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='download')),
                ('episodes_viewed', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='viewed')),
                ('times', models.PositiveSmallIntegerField(default=0, verbose_name='times watched')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='start in')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='end in')),
                ('link', models.URLField(blank=True, verbose_name='link')),
                ('note', models.DecimalField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='note', max_digits=2, blank=True, null=True, decimal_places=1)),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('anime', models.ForeignKey(verbose_name='anime', to='ergoanimes.Anime', related_name='useranimes')),
                ('fansub', models.ForeignKey(to='ergoanimes.Fansub', null=True, verbose_name='fansub', blank=True, related_name='useranimes')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='+')),
            ],
            options={
                'verbose_name_plural': 'users animes',
                'verbose_name': 'user anime',
                'ordering': ('user', 'anime'),
            },
        ),
        migrations.AddField(
            model_name='anime',
            name='genres',
            field=models.ManyToManyField(blank=True, verbose_name='genres', related_name='animes', to='ergoanimes.Genre'),
        ),
        migrations.AlterUniqueTogether(
            name='useranime',
            unique_together=set([('user', 'anime')]),
        ),
        migrations.RunPython(insert_genres),
    ]
