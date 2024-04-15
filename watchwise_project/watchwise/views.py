from .models import Movie, TVShow
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import FloatField
from django.db.models.functions import Cast
import requests


TMDB_API_KEY = "05e5be7a518e07b0cdd93bf0e133083a"


# Render the homepage
def watchwise(request):
    return render(request, 'homepage.html')
    

# Display a list of movies specific to the logged-in user
def movie_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    movies_list = Movie.objects.filter(user=request.user).order_by('movie_id')
    per_page = request.GET.get('per_page', '10')  
    page_number = request.GET.get('page', 1)  
    paginator = Paginator(movies_list, int(per_page)) 
    movies = paginator.get_page(page_number)
    return render(request, 'movie_list.html', {'movies': movies, 'per_page': per_page})


# Display a list of TV shows specific to the logged-in user
def tv_show_list(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    tv_shows_list = TVShow.objects.filter(user=request.user).order_by('TV_id') 
    per_page = request.GET.get('per_page', '10')  
    page_number = request.GET.get('page', 1)  
    paginator = Paginator(tv_shows_list, int(per_page))  
    tv_shows = paginator.get_page(page_number)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows, 'per_page': per_page})


# Handle search queries using the TMDB API
def results(request):
    query = request.GET.get('q')
    if query:
        data = requests.get(f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        data = data.json()

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
    

# Allow users to delete their media entries        
def delete_media(request, type, id):
    if not request.user.is_authenticated:
        return redirect('login')
    if type == 'movie':
        movie = get_object_or_404(Movie, movie_id=id, user=request.user)
        movie.delete()
    elif type == 'tv':
        tv_show = get_object_or_404(TVShow, TV_id=id, user=request.user)
        tv_show.delete()
    messages.success(request, "Deleted successfully")
    return redirect(request.META.get('HTTP_REFERER', 'default_if_none'))


# Allow users to update status, ratings, and comments on their media entries
def update_media(request, id, type):
    if type == 'movie':
        media = get_object_or_404(Movie, movie_id=id)
    elif type == 'tv':
        media = get_object_or_404(TVShow, TV_id=id)
    else:
        messages.error(request, "Invalid media type")
        return redirect('results')
    if request.method == 'POST':
        media.status = request.POST.get('status')
        rating = request.POST.get('rating')
        media.rating = None if rating == '' else rating
        media.comment = request.POST.get('comment')
        media.save()
        messages.success(request, "Updated successfully")
        return redirect('movie_list' if type == 'movie' else 'tv_show_list')
    else:
        return render(request, 'update_media.html', {'media': media})
        

# Allow users to add new media entries
def save_media(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        external_id = request.POST.get('external_id')
        media_type = request.POST.get('type')

        existing_media = Movie.objects.filter(user=request.user, external_id=external_id) if media_type == 'movie' else TVShow.objects.filter(user=request.user, external_id=external_id)
        if existing_media.exists():
            messages.info(request, "This media is already in your library.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        try:
            status = request.POST.get('status')
            rating = request.POST.get('rating', None)
            title = request.POST.get('title')
            date_str = request.POST.get('date')
            overview = request.POST.get('overview')
            original_language = request.POST.get('original_language')
            comment = request.POST.get('comment')
            rating = None if rating == '' else int(rating)
            date = int(date_str) if date_str else None

            media_details = {
                'user': request.user,
                'external_id': external_id,
                'title': title,
                'release_date' if media_type == 'movie' else 'first_air_date': date,
                'overview': overview,
                'original_language': original_language,
                'status': status,
                'rating': rating,
                'comment': comment
            }

            if media_type == 'movie':
                Movie.objects.create(**media_details)
            else:
                TVShow.objects.create(**media_details)

            messages.success(request, "Your media has been added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding media: {str(e)}")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "This method is not allowed.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    
# Helper function to paginate any queryset based on request parameters
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


# Search for movies by title
def search_title_movie(request):
    title = request.GET.get('title', '')
    movies = Movie.objects.filter(user=request.user, title__icontains=title)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Filter movies by status
def search_status_movie(request):
    status = request.GET.get('status', '')
    movies = Movie.objects.filter(user=request.user, status__icontains=status)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Filter movies by rating
def search_rating_movie(request):
    rating = request.GET.get('rating', '')
    if rating.isdigit():
        movies = Movie.objects.filter(user=request.user, rating=int(rating))
    else:
        movies = Movie.objects.filter(user=request.user)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Sort movies by title
def sort_movies_by_title(request):
    sort_by = request.GET.get('sort_title', 'title') 
    movies = Movie.objects.filter(user=request.user).order_by(sort_by)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Sort movies by release year
def sort_movies_by_year(request):
    sort_by = request.GET.get('sort_year', 'release_date')
    movies = Movie.objects.filter(user=request.user).order_by(sort_by)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Sort movies by rating
def sort_movies_by_rating(request):
    sort_by = request.GET.get('sort_rating', 'rating')
    if sort_by == 'rating':
        movies = Movie.objects.filter(user=request.user).annotate(rating_as_float=Cast('rating', FloatField())).order_by('rating_as_float')
    elif sort_by == '-rating':
        movies = Movie.objects.filter(user=request.user).annotate(rating_as_float=Cast('rating', FloatField())).order_by('-rating_as_float')
    else:
        movies = Movie.objects.filter(user=request.user)
    movies = paginate_queryset(request, movies)
    return render(request, 'movie_list.html', {'movies': movies})


# Search for TV shows by title
def search_title_tv(request):
    title = request.GET.get('title', '')
    tv_shows = TVShow.objects.filter(user=request.user, title__icontains=title)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


# Filter TV shows by status
def search_status_tv(request):
    status = request.GET.get('status', '')
    tv_shows = TVShow.objects.filter(user=request.user, status__icontains=status)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


# Filter TV shows by rating
def search_rating_tv(request):
    rating = request.GET.get('rating', '')
    if rating.isdigit():
        tv_shows = TVShow.objects.filter(user=request.user, rating=int(rating))
    else:
        tv_shows = TVShow.objects.filter(user=request.user)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


# Sort TV shows by title
def sort_tv_shows_by_title(request):
    sort_by = request.GET.get('sort_title', 'title')
    tv_shows = TVShow.objects.filter(user=request.user).order_by(sort_by)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})

# Sort TV shows by the year they first aired
def sort_tv_shows_by_year(request):
    sort_by = request.GET.get('sort_year', 'first_air_date')
    tv_shows = TVShow.objects.filter(user=request.user).order_by(sort_by)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


# Sort TV shows by rating
def sort_tv_shows_by_rating(request):
    sort_by = request.GET.get('sort_rating', 'rating')
    if sort_by == 'rating':
        tv_shows = TVShow.objects.filter(user=request.user).annotate(rating_as_float=Cast('rating', FloatField())).order_by('rating_as_float')
    elif sort_by == '-rating':
        tv_shows = TVShow.objects.filter(user=request.user).annotate(rating_as_float=Cast('rating', FloatField())).order_by('-rating_as_float')
    else:
        tv_shows = TVShow.objects.filter(user=request.user)
    tv_shows = paginate_queryset(request, tv_shows)
    return render(request, 'tv_show_list.html', {'tv_shows': tv_shows})


# Handle user registration using a form
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')

    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})
