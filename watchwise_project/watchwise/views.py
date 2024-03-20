from django.http import HttpResponse
from django.template import loader
from .models import Media, Type

def watchwise(request):
    template = loader.get_template('homepage.html')
    context = {}
    return HttpResponse(template.render(context=context))

def movies(request):
    movie_type = Type.objects.get(type='Movie')
    movies = Media.objects.filter(media_type=movie_type)

    template = loader.get_template('movies.html')
    context = {
        'movies': movies,
    }

    return HttpResponse(template.render(context=context))

def tv_shows(request):
    tv_show_type = Type.objects.get(type='TV Show')
    tv_shows = Media.objects.filter(media_type=tv_show_type)

    template = loader.get_template('tv_shows.html')
    context = {
        'tv_shows': tv_shows,
    }

    return HttpResponse(template.render(context=context))
