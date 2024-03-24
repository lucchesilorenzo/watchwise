from django.urls import path
from . import views

urlpatterns = [
    path('', views.watchwise, name='homepage'),
    path('movie_list', views.movie_list, name='movie_list'),
    path('tv_show_list', views.tv_show_list, name='tv_show_list'),
]
