from django.http import HttpResponse
from django.template import loader
from .models import Media

def homepage(request):
    media = Media.objects.all() # lista speciale 'QuerySet', istanze degli oggetti disponibili | con .values() non posso creare dei metodi, restitusce una lista di dizionari
    template = loader.get_template('homepage.html')
    context = {
        'media': media,
    }
    return HttpResponse(template.render(context=context))