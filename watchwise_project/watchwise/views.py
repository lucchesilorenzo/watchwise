from django.http import HttpResponse
from django.template import loader
from .models import Media, Type

def watchwise(request):
    template = loader.get_template('homepage.html')
    context = {}
    return HttpResponse(template.render(context=context))

def movies(request):
    movies = Media.objects.filter(media_type=1)

    template = loader.get_template('movies.html')
    context = {
        'movies': movies,
    }

    return HttpResponse(template.render(context=context))

def tv_shows(request):
    tv_shows = Media.objects.filter(media_type=2)

    template = loader.get_template('tv_shows.html')
    context = {
        'tv_shows': tv_shows,
    }

    return HttpResponse(template.render(context=context))

def anime(request):
    anime = Media.objects.filter(media_type=3)

    template = loader.get_template('anime.html')
    context = {
        'anime': anime,
    }

    return HttpResponse(template.render(context=context))

