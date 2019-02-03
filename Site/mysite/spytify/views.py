from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django_tables2 import RequestConfig
from django.db import connection
from django.http import HttpResponseRedirect
from .tables import PlayTable

from .models import Artist, Album, Song, Play, UserToken
from .forms import SignUpForm

import spotify_api.spotipy.oauth2 as oauth

import utils


def top(request):
    """
    View function for users to view their all time listening history from spotify's v1/me/top endpoint.

    :param request:
    :return:
    """
    context = {}
    if request.user.pk:
        token = UserToken.objects.get(user_id=request.user.pk).__dict__
        current_user = request.user
        top = utils.get_top_all_time(current_user, token)
        context = {**context, **top}
    return render(request, 'top_all_time.html', context=context)


def index(request):
    """
    View function for home page of site.

    :param request:
    :return:
    """
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
                name = Song.objects.get(song_id=song)
                # name = cursor.execute("SELECT * from 'spytify_song' WHERE song_id = '{}'".format(song)).fetchone()
                if name:
                    top_songs.append((name, plays))
                if len(top_songs) == 5:
                    break
            context['user_songs'] = top_songs

        with connection.cursor() as cursor:
            sp_authed = len(cursor.execute("""SELECT       *
                                            FROM     spytify_usertoken
                                            WHERE user_id = {}""".format(request.user.id)).fetchall())
        context['sp_authed'] = sp_authed


    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def signup(request):
    """
    View function for users to signup for the site.

    :param request:
    :return:
    """
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


def UserPlaysView(request):
    """
    View function for the users individual plays table.

    :param request:
    :return:
    """

    # check if user is authenticated
    if request.user.is_authenticated:
        plays = Play.objects.filter(user=request.user.pk)
        table = PlayTable(plays, order_by='-play_id')
        context = {
            'plays_table': table,
            'user': request.user
        }

        RequestConfig(request).configure(table)

        return render(request, 'user_plays_table.html', context=context)
    else:
        # redirect to the base page if we're not authenticated
        return HttpResponseRedirect('/')


def authedView(request):
    """
    View function for when the user has authorized the app

    This function parses the callback URL provided by spotify, and uses it to get the User's Token info

    :param request:
    :return:
    """
    # redirect_uri = 'http://127.0.0.1:8000/authed'
    redirect_uri = 'http://spyify.duckdns.org/authed'
    client_id = 'd85350c3c35449d987db695a8e5a819b'
    client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
    scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state user-top-read'

    oAuth2 = oauth.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, cache_path=r'spotify_api/token_cache/')

    token_info = oAuth2.get_access_token(request.GET['code'])
    user = request.user
    user_token = UserToken(user=user, access_token=token_info['access_token'], token_type=token_info['token_type'],
                           expires_in=token_info['expires_in'], scope=token_info['scope'],
                           expires_at=token_info['expires_at'], refresh_token=token_info['refresh_token'])
    user_token.save()
    oAuth2.save_token_info(token_info)
    return render(request, 'authed.html')


def TrackDetailView(request, trackid):
    """
    A view for gathering the data for an track's details page

    :param request:
    :param artistid:
    :return:
    """
    context = {'user': request.user}
    context['track'] = Song.objects.get(pk=trackid)

    return render(request, 'track.html', context=context)

def ArtistDetailView(request, artistid):
    """
    A view for gathering the data for an artist's details page

    :param request:
    :param artistid:
    :return:
    """
    context = {'user': request.user}
    context['artist'] = Artist.objects.get(pk=artistid)

    return render(request, 'artist.html', context=context)


