from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.watchwise, name='homepage'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('tv_show_list/', views.tv_show_list, name='tv_show_list'),
    path('results/', views.results, name='results'),
    path('save_media/', views.save_media, name='save_media'),
    path('delete_media/<str:type>/<int:id>/', views.delete_media, name='delete_media'),
    path('update_media/<str:type>/<int:id>/', views.update_media, name='update_media'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]