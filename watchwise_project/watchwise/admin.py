from django.contrib import admin
from .models import Genre, Type, Media, Profile


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'genre')


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'media_type', 'genre', 'release_year')
    list_filter = ('media_type', 'genre')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'birth_date')
    list_filter = ('user', 'birth_date')
