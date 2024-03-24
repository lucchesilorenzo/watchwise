from .models import Media
from django.shortcuts import render
import requests
from django.http import HttpResponse
from datetime import datetime

# Define the API key for The Movie Database
TMDB_API_KEY = "05e5be7a518e07b0cdd93bf0e133083a"

def watchwise(request):
    return render(request, 'homepage.html')

# View for the homepage
def watchwise(request):
    # Render the homepage template
    return render(request, 'homepage.html')

# View for movies
def results(request):
    # Get the query from the search box
    query = request.GET.get('q')

    # If the query is not empty
    if query:
        # Get the results from the API
        data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        data = data.json()

        # Convert release_date and first_air_date to just the year
        for m in data['results']:
            if 'release_date' in m and m['release_date']:
                m['release_date'] = datetime.strptime(m['release_date'], '%Y-%m-%d').year
            if 'first_air_date' in m and m['first_air_date']:
                m['first_air_date'] = datetime.strptime(m['first_air_date'], '%Y-%m-%d').year

    else:
        # If the query is empty, return a message
        return HttpResponse("Please enter a search query")

    # Render the movies template with the data from the API
    return render(request, 'results.html', {
        "data": data,
        "type": request.GET.get("type")
    })

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
