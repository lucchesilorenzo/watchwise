from django.contrib import admin
from .models import Media, Type, Genre, Profile

class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "genre",)

admin.site.register(Media, MediaAdmin)
admin.site.register(Type)
admin.site.register(Genre)

admin.site.register(Profile)