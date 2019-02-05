import django_tables2 as tables

from .models import User, Artist, Album, Song, Play


class PlayTable(tables.Table):
    """
    A table class for displaying a list of plays
    """

    class Meta:
        model = Play
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('play_id', 'time_stamp', 'song', 'song.artist_id', 'song.album_id')


class TrackTable(tables.Table):
    """
    A table class for displaying a list of plays
    """

    class Meta:
        model = Play
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('play_id', 'time_stamp', 'song', 'song.artist_id', 'song.album_id')