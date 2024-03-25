from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    genre = models.CharField(max_length=10)

    def __str__(self):
        return self.genre
    

class Type(models.Model):
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.type


class Media(models.Model):
    title = models.CharField(max_length=255)
    media_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_year = models.IntegerField()

    def __str__(self): 
        return self.title
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + '(' + self.user.username + ') - ' + str(self.birth_date)
    

STATUS_CHOICES = [
    ('already_seen', 'Already Seen'),
    ('wishlist', 'Wishlist'),
    ('not_interested', 'Not Interested'),
]


class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_date = models.IntegerField()
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='wishlist')
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)


class TV_Shows(models.Model):
    TV_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    first_air_date = models.IntegerField()
    overview = models.TextField()
    original_language = models.CharField(max_length=2)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='wishlist')
    rating = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
