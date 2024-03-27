from django.contrib import admin
from .models import Profile, Movie, TVShow

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

    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'birth_date')
    list_filter = ('user', 'birth_date')
