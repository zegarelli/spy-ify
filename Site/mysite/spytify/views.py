from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django_tables2 import RequestConfig

from spytify.models import User, Artist, Album, Song, Play
from spytify.tables import PlayTable


"""------------------------------------------------------------
-
-   MODEL NAME: index
-
-   DESCRIPTION: View function for home page of site.
-
------------------------------------------------------------"""
def index(request):
    # Generate counts of some of the main objects
    num_users   = User.objects.all().count()
    num_artists = Artist.objects.all().count()
    num_albums  = Album.objects.all().count()
    num_songs   = Song.objects.all().count()
    num_plays   = Play.objects.all().count()
    
    context = {
        'num_users'  : num_users,
        'num_artists': num_artists,
        'num_albums' : num_albums,
        'num_songs'  : num_songs,
        'num_plays'  : num_plays,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

"""END def index"""

"""------------------------------------------------------------
-
-   MODEL NAME: UserDetailView
-
-   DESCRIPTION: View function for user details of site.
-
------------------------------------------------------------"""
def UserDetailView(request, userid):
    table = PlayTable( Play.objects.filter( user__user_id__contains = userid ) )
    RequestConfig(request).configure(table)
    return render( request, 'user_detail_table.html', { 'user':table } )

"""END def UserDetailView"""