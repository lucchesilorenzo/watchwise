from django.shortcuts import render
from .models import Media

def watchwise(request):
    return render(request, 'homepage.html')

def movies(request):
    movies = Media.objects.filter(media_type=1)
    context = {
        'movies': movies,
    }
    return render(request, 'movies.html', context)

def tv_shows(request):
    tv_shows = Media.objects.filter(media_type=2)
    context = {
        'tv_shows': tv_shows,
    }
    return render(request, 'tv_shows.html', context)

def anime(request):
    anime = Media.objects.filter(media_type=3)
    context = {
        'anime': anime,
    }
    return render(request, 'anime.html', context)