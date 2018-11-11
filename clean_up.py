# To make this script work, first open up node.js command prompt and cd to:
#     C:\Users\Martin\Google Drive\Python\Spotify\njtest
# then call:
#     node server.js
# then run this script

import spotipy
import spotipy.util as util
import datetime
import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar

import pdb

def get_sheet(sheet_name):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    new_sheet = client.open("Spotify_Tracking").worksheet(sheet_name)
    return new_sheet

def add_song_to_database(id, unique_songs, artist_id, album_id):
    if not unique_songs:
        unique_songs = get_sheet('Unique_Songs')
        records = unique_songs.get_all_records()
    if not id_in_database(id, records):
        f = sp.audio_features(id)[0]
        unique_songs.insert_row([id, f['danceability'], f['energy'], f['key'], f['loudness'], f['mode'], f['speechiness'],
                           f['acousticness'], f['instrumentalness'], f['liveness'], f['valence'], f['tempo'], f['type'],
                           f['duration_ms'], f['time_signature'], artist_id, album_id], 2)
        # add_artist_to_database(artist_id, unique_artists)
        # add_album_to_database(album_id, unique_albums)

def add_artist_to_database(id, unique_artists):
    if not unique_artists:
        unique_artists = get_sheet('Unique_Artists')
        records = unique_artists.get_all_records()
    if not id_in_database(id, records):
        f = sp.artist(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        unique_artists.insert_row([id, f['name'], genres[:-2], f['followers']['total'], f['popularity']], 2)
        print(f['name'])

def add_album_to_database(id, unique_album):
    if not unique_album:
        unique_album = get_sheet('Unique_Albums')
        records = unique_album.get_all_records()
    if not id_in_database(id, records):
        f = sp.album(id)
        genres = ''
        for genre in f['genres']:
            genres += genre + ', '
        unique_album.insert_row([id, f['name'], f['artists'][0]['id'], f['label'], f['popularity'],
                                 f['album_type'], f['release_date'], genres[:-2], f['uri']], 2)
        print(f['name'])

def id_in_database(id, database):
    for item in database:
        if item['ID'] == id:
            return item
    return None

def find_track(sp, track_id):
    track = sp.track(track_id=track_id)
    return track

if __name__ == '__main__':
    unique_songs = None
    unique_artists = None
    unique_albums = None
    client_id = 'd85350c3c35449d987db695a8e5a819b'
    client_secret = '516a6cd7008b4c3f8aa41d800a2415a0'
    redirect_uri = 'http://localhost:8888/callback'
    username = 'prepxc@gmail.com'
    scopes = 'user-read-currently-playing user-library-read user-read-recently-played user-read-playback-state'

    token = util.prompt_for_user_token(username, scope=scopes, client_id=client_id,
                                       client_secret=client_secret, redirect_uri=redirect_uri)
    if token:
        sp = spotipy.Spotify(auth=token)
        # sheet = get_sheet('All_Plays')
        # records = sheet.get_all_records()
        # for n, row in enumerate(records):
        #     if n > 457:
        #         track = sp.track(row['ID'])
        #         add_song_to_database(row['ID'], unique_songs, track['artists'][0]['id'], track['album']['id'])
        #         print(n)



        sheet = get_sheet('Unique_Songs')
        records = sheet.get_all_records()
        for n, row in enumerate(records):
            if n > 10:
                track = sp.track(row['ID'])
                sheet.update_cell(n+2, 18, track['name'])
                time.sleep(1)
                sheet.update_cell(n+2, 19, track['popularity'])
                time.sleep(1)
        #         add_artist_to_database(track['artists'][0]['id'], unique_artists)
        #         time.sleep(1)
        #         add_album_to_database(track['album']['id'], unique_albums)
            # print(track)



    else:
        print("Can't get token for", username)

