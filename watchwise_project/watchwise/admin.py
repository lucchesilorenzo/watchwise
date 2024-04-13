from django.contrib import admin
from .models import Movie, TVShow


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'movie_id',
        'title',
        'release_date',
        'overview',
        'original_language',
        'status',
        'rating',
        'comment',
    )


@admin.register(TVShow)
class TVShowAdmin(admin.ModelAdmin):
    list_display = (
        'TV_id',
        'title',
        'first_air_date',
        'overview',
        'original_language',
        'status',
        'rating',
        'comment',
    )
