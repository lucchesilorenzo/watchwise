from django.db import models
    
    
STATUS_CHOICES = [
    ('empty', 'None'),
    ('watched', 'Watched'),
    ('watchlist', 'Watchlist'),
    ('not_interested', 'Not Interested'),
]


class Movie(models.Model):
    external_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_date = models.IntegerField(null=True, blank=True)
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='empty')
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)


class TVShow(models.Model):
    external_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    TV_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    first_air_date = models.IntegerField(null=True, blank=True)
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='empty')
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
