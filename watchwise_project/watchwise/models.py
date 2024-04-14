from django.db import models
from django.conf import settings
    
# Define status choices for media items
STATUS_CHOICES = [
    ('empty', 'None'),
    ('watched', 'Watched'),
    ('watchlist', 'Watchlist'),
    ('not_interested', 'Not Interested'),
]


class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movies', null=True)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_date = models.IntegerField(null=True, blank=True)
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='empty')
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    # Ensure uniqueness of external_id per user
    class Meta:
        unique_together = ('user', 'external_id')


class TVShow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tv_shows', null=True)
    external_id = models.CharField(max_length=100, null=True, blank=True)
    TV_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    first_air_date = models.IntegerField(null=True, blank=True)
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='empty')
    rating = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    # Ensure uniqueness of external_id per user
    class Meta:
        unique_together = ('user', 'external_id')
