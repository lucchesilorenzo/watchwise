from django.db import models

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
    