from django.db import models
from django.contrib.auth.models import User
"""------------------------------------------------------------
-
-   MODEL NAME: User
-
-   DESCRIPTION: Model representing a user profile
-
------------------------------------------------------------"""
# class UserProfile(models.Model):

    #****************************
    #         Members
    #****************************
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField()
    # first_name = models.CharField(max_length=50, null=True, blank=True)
    # last_name = models.CharField(max_length=50, null=True, blank=True)
    # sex = models.CharField(max_length=50, null=True, blank=True)
    # birthday = models.DateField(null=True, blank=True)
    # date_joined = models.DateField(null=True, blank=True)

    # """----------------------------------------------
    # - NAME: __str__()
    # -
    # - DESCRIPTION: standard Python class method to
    # -              return a human-readable string for
    # -              User object
    # ----------------------------------------------"""
    # def __str__(self):
        # return '{} {}: {}'.format(self.first_name, self.last_name, self.email)

"""END class User"""

"""------------------------------------------------------------
-
-   MODEL NAME: Artist
-
-   DESCRIPTION: Model representing a music artist on the service
-
------------------------------------------------------------"""
class Artist(models.Model):

    #****************************
    #         Members
    #****************************
    artist_id = models.CharField(max_length=50, primary_key=True)
    artist_name = models.CharField(max_length=100, null=True, blank=True)
    genres = models.CharField(max_length=100, null=True, blank=True)
    followers = models.IntegerField(null=True, blank=True)
    artist_popularity = models.IntegerField(null=True, blank=True)

    """----------------------------------------------
    - NAME: __str__()
    -
    - DESCRIPTION: standard Python class method to 
    -              return a human-readable string for 
    -              Artist object
    ----------------------------------------------"""
    def __str__(self):
        return self.artist_name

"""END class Artist"""

"""------------------------------------------------------------
-
-   MODEL NAME: Album
-
-   DESCRIPTION: Model representing an album on the service
-
------------------------------------------------------------"""
class Album(models.Model):

    #****************************
    #         Members
    #****************************
    album_id = models.CharField(max_length=50, primary_key=True)
    album_name = models.CharField(max_length=100, null=True, blank=True)
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, null=True, blank=True)
    album_popularity = models.IntegerField(null=True, blank=True)
    album_type = models.CharField(max_length=100, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    """----------------------------------------------
    - NAME: __str__()
    -
    - DESCRIPTION: standard Python class method to 
    -              return a human-readable string for 
    -              Album object
    ----------------------------------------------"""
    def __str__(self):
        return self.album_name

"""END class Album"""

"""------------------------------------------------------------
-
-   MODEL NAME: Song
-
-   DESCRIPTION: Model representing a song one can listen to
-
------------------------------------------------------------"""
class Song(models.Model):

    #****************************
    #         Members
    #****************************
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

    """----------------------------------------------
    - NAME: __str__()
    -
    - DESCRIPTION: standard Python class method to 
    -              return a human-readable string for 
    -              Song object
    ----------------------------------------------"""
    def __str__(self):
        return self.song_name

"""END class Song"""

"""------------------------------------------------------------
-
-   MODEL NAME: Play
-
-   DESCRIPTION: Model representing a play instance of a song
-                by a user.
-
------------------------------------------------------------"""
class Play(models.Model):

    #****************************
    #         Members
    #****************************
    play_id = models.BigAutoField(primary_key=True)
    time_stamp = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    device = models.CharField(max_length=50, null=True, blank=True)

    """----------------------------------------------
    - NAME: __str__()
    -
    - DESCRIPTION: standard Python class method to 
    -              return a human-readable string for 
    -              Play object
    ----------------------------------------------"""
    def __str__(self):
        return '{} {}: {}'.format(self.time_stamp, self.user, self.song)

"""END class Play"""
