from django.urls import path
from . import views

urlpatterns = [
    path('', views.watchwise, name='homepage'),
    path('movies', views.movies, name='movies'),
    path('tv_shows', views.tv_shows, name='tv_shows'),
]
