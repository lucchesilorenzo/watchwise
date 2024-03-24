from django.shortcuts import render
from .models import Media

def watchwise(request):
    return render(request, 'homepage.html')

def movie_list(request):
    movies = Media.objects.filter(media_type=1)
    context = {
        'movies': movies,
    }
    return render(request, 'movie_list.html', context)

def tv_show_list(request):
    tv_shows = Media.objects.filter(media_type=2)
    context = {
        'tv_shows': tv_shows,
    }
    return render(request, 'tv_show_list.html', context)
