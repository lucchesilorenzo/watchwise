from django.http import HttpResponse
from django.template import loader
from .models import Media

def homepage(request):
    media = Media.objects.all()
    template = loader.get_template('homepage.html')