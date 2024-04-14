from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', views.watchwise, name='homepage'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('tv_show_list/', views.tv_show_list, name='tv_show_list'),
    path('results/', views.results, name='results'),
    path('save_media/', views.save_media, name='save_media'),
    path('delete_media/<str:type>/<int:id>', views.delete_media, name='delete_media'),
    path('update_media/<str:type>/<int:id>', views.update_media, name='update_media'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),
    path('search_title_movie/', views.search_title_movie, name='search_title_movie'),
    path('search_status_movie/', views.search_status_movie, name='search_status_movie'),
    path('search_rating_movie/', views.search_rating_movie, name='search_rating_movie'),
    path('sort_movies_by_title/', views.sort_movies_by_title, name='sort_movies_by_title'),
    path('sort_movies_by_year/', views.sort_movies_by_year, name='sort_movies_by_year'),
    path('sort_movies_by_rating/', views.sort_movies_by_rating, name='sort_movies_by_rating'),
    path('search_title_tv/', views.search_title_tv, name='search_title_tv'),
    path('search_status_tv/', views.search_status_tv, name='search_status_tv'),
    path('search_rating_tv/', views.search_rating_tv, name='search_rating_tv'),
    path('sort_tv_shows_by_title/', views.sort_tv_shows_by_title, name='sort_tv_shows_by_title'),
    path('sort_tv_shows_by_year/', views.sort_tv_shows_by_year, name='sort_tv_shows_by_year'),
    path('sort_tv_shows_by_rating/', views.sort_tv_shows_by_rating, name='sort_tv_shows_by_rating'),
]
