from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django_tables2 import RequestConfig
from django.db import connection

from .tables import PlayTable

from .models import Artist, Album, Song, Play, User
from .forms import SignUpForm

import utils
"""------------------------------------------------------------
-
-   VIEW NAME: top_all_time
-
-   DESCRIPTION: View function for users to view their all time
-                listening history from spotify's  v1/me/top
-                endpoint. 
------------------------------------------------------------"""
def top(request):
    context = {}
    if request.user.pk:
        current_user = request.user
        top = utils.get_top_all_time(current_user.email)
        context = {**context, **top}
    return render(request, 'top_all_time.html', context=context)

"""END def signup"""
"""------------------------------------------------------------
-
-   VIEW NAME: index
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
        'num_users': num_users,
        'num_artists': num_artists,
        'num_albums': num_albums,
        'num_songs': num_songs,
        'num_plays': num_plays,
    }

    # Generate Data for the Current User
    if request.user.pk:
        with connection.cursor() as cursor:
            user_songs = cursor.execute("""SELECT       song_id,
                                            COUNT(song_id) AS value_occurrence
                                            FROM     spytify_play
                                            WHERE user_id = {}
                                            GROUP BY song_id
                                            ORDER BY value_occurrence DESC
                                            LIMIT    50;""".format(request.user.id)).fetchall()
            top_songs = []
            for song, plays in user_songs:
                name = cursor.execute("SELECT song_name from 'spytify_song' WHERE song_id = '{}'".format(song)).fetchone()
                if name:
                    top_songs.append((name[0], plays))
                if len(top_songs) == 5:
                    break
        context['user_songs'] = top_songs


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

"""END def index"""

"""------------------------------------------------------------
-
-   VIEW NAME: signup
-
-   DESCRIPTION: View function for users to signup for the site.
-
------------------------------------------------------------"""
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

"""END def signup"""

"""------------------------------------------------------------
-   MODEL NAME: UserDetailView
-
-   DESCRIPTION: View function for user details of site.
-
------------------------------------------------------------"""
def UserDetailView(request, userid):
    table = PlayTable(Play.objects.filter(user__id__contains=userid))
    RequestConfig(request).configure(table)
    return render(request, 'user_detail_table.html', {'user': table})

"""END def UserDetailView"""

