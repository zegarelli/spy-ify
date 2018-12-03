import django_tables2 as tables

from .models import User, Artist, Album, Song, Play

"""------------------------------------------------------------
-
-   CLASS NAME: PlayTable
-
-   DESCRIPTION: Play Table class def for rendering out user's
-                play data into a nice table
-
------------------------------------------------------------"""
class PlayTable(tables.Table):
    class Meta:
        model = Play
        template_name = 'django_tables2/bootstrap4.html'
        fields = ('time_stamp', 'song', 'device')

"""END class PlayTable"""