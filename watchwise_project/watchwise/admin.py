from django.contrib import admin
from .models import Movie, TVShow


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'external_id',
        'movie_id',
        'title',
        'release_date',
        'overview',
        'original_language',
        'status',
        'rating',
        'comment',
    )
    list_filter = ('user',)


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'external_id',
        'TV_id',
        'title',
        'first_air_date',
        'overview',
        'original_language',
        'status',
        'rating',
        'comment',
    )
    list_filter = ('user',)