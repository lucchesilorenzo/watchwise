from .models import Movie, TVShow
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import requests
from django.core.paginator import Paginator
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.contrib.auth import login
from .forms import RegistrationForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


TMDB_API_KEY = "05e5be7a518e07b0cdd93bf0e133083a"


def watchwise(request):
    return render(request, 'homepage.html')
    

def movie_list(request):
    movies_list = Movie.objects.all().order_by('movie_id')
    per_page = request.GET.get('per_page', '10')  # Keep it as a string
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided

    paginator = Paginator(movies_list, int(per_page))  # Convert to int here
    movies = paginator.get_page(page_number)

    return render(request, 'movie_list.html', {'movies': movies, 'per_page': per_page})


def tv_show_list(request):
    tv_shows_list = TVShow.objects.all().order_by('TV_id')
    per_page = request.GET.get('per_page', '10')  # Keep it as a string
    page_number = request.GET.get('page', 1)  # Default to page 1 if not provided

    paginator = Paginator(tv_shows_list, int(per_page))  # Convert to int here
    tv_shows = paginator.get_page(page_number)

    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows, 'per_page': per_page})

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
        tv_show = get_object_or_404(TVShow, TV_id=id)
        tv_show.delete()
    messages.success(request, "Deleted Successfully")
    return redirect(request.META.get('HTTP_REFERER', 'default_if_none'))


def update_media(request, id, type):
    if type == 'movie':
        media = get_object_or_404(Movie, movie_id=id)
    elif type == 'tv':
        media = get_object_or_404(TVShow, TV_id=id)
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
        date_str = request.POST.get('date')  # Get the date as a string
        overview = request.POST.get('overview')
        original_language = request.POST.get('original_language')
        comment = request.POST.get('comment')

        # Try to convert the date string to an integer, handling cases where it is None or invalid
        try:
            date = int(date_str) if date_str is not None else None
        except ValueError:
            messages.error(request, "Invalid date provided.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        if not date:
            messages.error(request, "Date is required.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
            tv_show, created = TVShow.objects.get_or_create(
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

        messages.success(request, "Your media has been saved successfully!")
        # Redirect back to the referring page instead of going to the homepage
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "Invalid request method.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

def paginate_queryset(request, queryset, default_per_page=10):
    per_page = request.GET.get('per_page', '')
    if not per_page.isdigit():
        per_page = default_per_page
    else:
        per_page = int(per_page)
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def search_title_movie(request):
    title = request.GET.get('title', '')
    movies = Movie.objects.filter(title__icontains=title)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


def search_status_movie(request):
    status = request.GET.get('status', '')
    movies = Movie.objects.filter(status__icontains=status)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})

def search_rating_movie(request):
    rating = request.GET.get('rating', '')
    if rating.isdigit():
        movies = Movie.objects.filter(rating=int(rating))
    else:
        movies = Movie.objects.all()
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


def sort_movies_by_title(request):
    sort_by = request.GET.get('sort_title', 'title')  # Default sort is by title
    movies = Movie.objects.all().order_by(sort_by)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})

def sort_movies_by_year(request):
    sort_by = request.GET.get('sort_year', 'release_date')  # Default sort is by release_date
    movies = Movie.objects.all().order_by(sort_by)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


def sort_movies_by_rating(request):
    sort_by = request.GET.get('sort_rating', 'rating')  # Default sort is by rating
    if sort_by == 'rating':
        movies = Movie.objects.annotate(rating_as_float=Cast('rating', FloatField())).order_by('rating_as_float')
    elif sort_by == '-rating':
        movies = Movie.objects.annotate(rating_as_float=Cast('rating', FloatField())).order_by('-rating_as_float')
    else:
        movies = Movie.objects.all()
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


def search_title_tv(request):
    title = request.GET.get('title', '')
    tv_shows = TVShow.objects.filter(title__icontains=title)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def search_status_tv(request):
    status = request.GET.get('status', '')
    tv_shows = TVShow.objects.filter(status__icontains=status)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def search_rating_tv(request):
    rating = request.GET.get('rating', '')
    if rating.isdigit():
        tv_shows = TVShow.objects.filter(rating=int(rating))
    else:
        tv_shows = TVShow.objects.all()
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def sort_tv_shows_by_title(request):
    sort_by = request.GET.get('sort_title', 'title')  # Default sort is by title
    tv_shows = TVShow.objects.all().order_by(sort_by)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def sort_tv_shows_by_year(request):
    sort_by = request.GET.get('sort_year', 'first_air_date')  # Default sort is by first_air_date
    tv_shows = TVShow.objects.all().order_by(sort_by)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def sort_tv_shows_by_rating(request):
    sort_by = request.GET.get('sort_rating', 'rating')  # Default sort is by rating
    if sort_by == 'rating':
        tv_shows = TVShow.objects.annotate(rating_as_float=Cast('rating', FloatField())).order_by('rating_as_float')
    elif sort_by == '-rating':
        tv_shows = TVShow.objects.annotate(rating_as_float=Cast('rating', FloatField())).order_by('-rating_as_float')
    else:
        tv_shows = TVShow.objects.all()
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'login.html')

    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})
