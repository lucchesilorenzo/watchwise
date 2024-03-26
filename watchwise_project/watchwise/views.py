from .models import Movie, TV_Shows, Media
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import requests


# Define the API key for The Movie Database
TMDB_API_KEY = "05e5be7a518e07b0cdd93bf0e133083a"


def watchwise(request):
    return render(request, 'homepage.html')
    

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


def tv_show_list(request):
    tv_shows = TV_Shows.objects.all()
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def results(request):
    # Handle the search query
    query = request.GET.get('q')
    if query:
        data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        data = data.json()

        # Filter out movies/TV shows without an image
        data['results'] = [m for m in data['results'] if m['poster_path'] is not None]

        for m in data['results']:
            if 'release_date' in m and m['release_date']:
                m['release_date'] = int(m['release_date'].split('-')[0])
            if 'first_air_date' in m and m['first_air_date']:
                m['first_air_date'] = int(m['first_air_date'].split('-')[0])

        return render(request, 'results.html', {
            "data": data,
            "type": request.GET.get("type")
        })

    else:
        return render(request, 'homepage.html', {"show_alert": True})
    
        
def delete_media(request, type, id):
    if type == 'movie':
        movie = get_object_or_404(Movie, movie_id=id)
        movie.delete()
    elif type == 'tv':
        tv_show = get_object_or_404(TV_Shows, TV_id=id)
        tv_show.delete()
    messages.success(request, "Deleted Successfully")
    return redirect(request.META.get('HTTP_REFERER', 'default_if_none'))


def update_media(request, id, type):
    if type == 'movie':
        media = get_object_or_404(Movie, movie_id=id)
    elif type == 'tv':
        media = get_object_or_404(TV_Shows, TV_id=id)
    else:
        messages.error(request, "Invalid media type")
        return redirect('results')

    if request.method == 'POST':
        # Update the media object
        media.status = request.POST.get('status')
        media.rating = request.POST.get('rating')
        media.comment = request.POST.get('comment')
        media.save()
        messages.success(request, "Updated Successfully")
        
        # Redirect to the appropriate list page based on the media type
        if type == 'movie':
            return redirect('movie_list')
        elif type == 'tv':
            return redirect('tv_show_list')
    else:
        # Render the update form
        return render(request, 'update_media.html', {'media': media})
    
        
def save_media(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        rating = request.POST.get('rating')
        TV_id = request.POST.get('TV_id')
        type = request.POST.get('type')
        title = request.POST.get('title')
        date = int(request.POST.get('date'))  # directly convert to int
        overview = request.POST.get('overview')
        original_language = request.POST.get('original_language')
        comment = request.POST.get('comment')

        if type == 'movie':
            movie, created = Movie.objects.get_or_create(
                movie_id=TV_id, 
                defaults={
                    'title': title, 
                    'release_date': date, 
                    'overview': overview, 
                    'original_language': original_language, 
                    'status': status, 
                    'rating': rating,
                    'comment': comment
                }
            )

            if not created:
                movie.status = status
                movie.rating = rating
                movie.comment = comment
                movie.save()
        elif type == 'tv':
            tv_show, created = TV_Shows.objects.get_or_create(
                TV_id=TV_id, 
                defaults={
                    'title': title, 
                    'first_air_date': date, 
                    'overview': overview, 
                    'original_language': original_language, 
                    'status': status, 
                    'rating': rating,
                    'comment': comment
                }
            )
            
            if not created:
                tv_show.status = status
                tv_show.rating = rating
                tv_show.comment = comment
                tv_show.save()
        return redirect('results')



# New - NOT WORKING
def inserimento(request):
    if request.POST:
        print(request.POST)

        title = request.POST['title']
        release_year = request.POST['release_year']

        q = Media(title=title, release_year=release_year)
        q.save()

        context = {
            'title': title,
            'release_year': release_year,
            'message': 'Salvato con successo',
        }

    else:
        context = {
            'message': '',
        }
    return render(request, 'inserimento.html', context)