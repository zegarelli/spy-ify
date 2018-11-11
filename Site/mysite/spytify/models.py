from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    date_joined = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} {}: {}'.format(self.first_name, self.last_name, self.email)


class Artist(models.Model):
    artist_id = models.CharField(max_length=50, primary_key=True)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    genres = models.CharField(max_length=100, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    artist_popularity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.artist_name


class Album(models.Model):
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
    play_id = models.BigAutoField(primary_key=True)
    time_stamp = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    device = models.CharField(max_length=50, null=True, blank=True)


