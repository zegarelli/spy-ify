from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    """
    Model representing a user's Spotify Token
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token =  models.CharField(max_length=200, null=True, blank=True)
    token_type = models.CharField(max_length=50, null=True, blank=True)
    expires_in = models.IntegerField(null=True, blank=True)
    scope = models.CharField(max_length=200, null=True, blank=True)
    expires_at = models.IntegerField(null=True, blank=True)
    refresh_token = models.CharField(max_length=200, null=True, blank=True)


class Artist(models.Model):
    """
    Model representing a music artist
    """
    artist_id = models.CharField(max_length=50, primary_key=True)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    genres = models.CharField(max_length=100, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    artist_popularity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.artist_name

class Album(models.Model):
    """
    Model representing an album
    """
    album_id = models.CharField(max_length=50, primary_key=True)
    album_name = models.CharField(max_length=100, null=True, blank=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, null=True, blank=True)
    album_popularity = models.IntegerField(null=True, blank=True)
    album_type = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.album_name

class Song(models.Model):
    """
    Model representing a spotify track
    """
    song_id = models.CharField(max_length=50, primary_key=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100)
    song_popularity = models.IntegerField(null=True, blank=True)
    danceability = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    key = models.IntegerField(null=True, blank=True)
    loudness = models.FloatField(null=True, blank=True)
    mode = models.IntegerField(null=True, blank=True)
    speechiness = models.FloatField(null=True,blank=True)
    acousticness = models.FloatField(null=True,blank=True)
    instrumentalness = models.FloatField(null=True, blank=True)
    liveness = models.FloatField(null=True, blank=True)
    valence = models.FloatField(null=True, blank=True)
    tempo = models.FloatField(null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    duration_ms = models.IntegerField(null=True, blank=True)
    time_signature = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.song_name


class Play(models.Model):
    """
    Model representing a play instance of a song by a user
    """
    play_id = models.BigAutoField(primary_key=True)
    time_stamp = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    device = models.CharField(max_length=50, null=True, blank=True)
    context = models.CharField(max_length=100, null=True, blank=True)
    context_type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '{} {}: {}'.format(self.time_stamp, self.user, self.song)